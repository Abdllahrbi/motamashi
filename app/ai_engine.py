import openai
from typing import List, Dict, Any
from datetime import datetime
import numpy as np
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class AITaskManager:
    def __init__(self):
        self.llm = OpenAI()
        self.task_analysis_prompt = PromptTemplate(
            input_variables=["title", "description"],
            template="""
            Analyze this task and provide a priority score between 0 and 1:
            Title: {title}
            Description: {description}
            
            Consider:
            1. Urgency of the task
            2. Complexity
            3. Dependencies
            4. Impact on project
            
            Return only the numerical score.
            """
        )
        
    async def analyze_task(self, title: str, description: str) -> float:
        """Analyze a task and return an AI-generated priority score."""
        chain = LLMChain(llm=self.llm, prompt=self.task_analysis_prompt)
        result = await chain.arun(title=title, description=description)
        try:
            return float(result.strip())
        except:
            return 0.5  # Default score if parsing fails
    
    async def get_recommendations(self, tasks: List[Any]) -> List[Dict[str, Any]]:
        """Generate task recommendations based on current tasks."""
        recommendations = []
        task_embeddings = []
        
        # Generate embeddings for tasks
        for task in tasks:
            response = await openai.Embedding.create(
                input=f"{task.title} {task.description}",
                model="text-embedding-ada-002"
            )
            task_embeddings.append(response['data'][0]['embedding'])
        
        # Cluster tasks and generate recommendations
        if task_embeddings:
            clusters = self._cluster_tasks(task_embeddings)
            for cluster in clusters:
                similar_tasks = [tasks[i] for i in cluster]
                recommendation = await self._generate_recommendation(similar_tasks)
                recommendations.append(recommendation)
        
        return recommendations
    
    def _cluster_tasks(self, embeddings: List[List[float]], threshold: float = 0.8) -> List[List[int]]:
        """Cluster tasks based on their embeddings."""
        clusters = []
        n_tasks = len(embeddings)
        used = set()
        
        for i in range(n_tasks):
            if i in used:
                continue
                
            cluster = [i]
            used.add(i)
            
            for j in range(i + 1, n_tasks):
                if j in used:
                    continue
                    
                similarity = np.dot(embeddings[i], embeddings[j])
                if similarity >= threshold:
                    cluster.append(j)
                    used.add(j)
                    
            clusters.append(cluster)
            
        return clusters
    
    async def _generate_recommendation(self, similar_tasks: List[Any]) -> Dict[str, Any]:
        """Generate a recommendation based on a cluster of similar tasks."""
        tasks_text = "\n".join([f"- {task.title}" for task in similar_tasks])
        
        prompt = f"""
        Based on these similar tasks:
        {tasks_text}
        
        Generate a recommendation for task optimization. Consider:
        1. Common patterns
        2. Potential automation
        3. Resource allocation
        4. Timeline optimization
        
        Return a JSON with 'title' and 'description' keys.
        """
        
        response = await openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a task optimization expert."},
                {"role": "user", "content": prompt}
            ]
        )
        
        try:
            return eval(response.choices[0].message.content)
        except:
            return {
                "title": "Task Optimization",
                "description": "Consider grouping these similar tasks for better efficiency."
            }
    
    async def generate_productivity_report(self, workspace_id: int, user_id: int) -> str:
        """Generate an AI-powered productivity report."""
        # This would typically analyze task completion rates, patterns, and provide insights
        # For now, we'll return a placeholder
        return """
        Productivity Analysis:
        1. Task Completion Rate: 85%
        2. Peak Productivity Hours: 10 AM - 2 PM
        3. Most Productive Days: Tuesday, Wednesday
        4. Recommendations:
           - Consider batch processing similar tasks
           - Schedule complex tasks during peak hours
           - Set up automated workflows for repetitive tasks
        """
