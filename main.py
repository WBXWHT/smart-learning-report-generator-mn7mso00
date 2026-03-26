import json
import random
import datetime
from typing import Dict, List, Any

class LearningReportGenerator:
    """智能学情报告生成器"""
    
    def __init__(self):
        """初始化报告生成器"""
        self.student_data_template = {
            "student_id": "",
            "student_name": "",
            "subject": "",
            "recent_scores": [],
            "attendance_rate": 0.0,
            "homework_completion": 0.0,
            "class_interaction": 0
        }
    
    def simulate_llm_api_call(self, prompt: str) -> str:
        """模拟大模型API调用（实际项目中替换为真实API）
        
        Args:
            prompt: 给大模型的提示词
            
        Returns:
            str: 生成的报告内容
        """
        # 模拟大模型生成不同风格的报告
        report_templates = [
            "根据学情数据分析，{name}同学在{subject}学科表现{performance}。近期成绩趋势{trend}，"
            "出勤率{attendance}%，作业完成率{homework}%。建议：{advice}",
            
            "{name}同学的{subject}学习报告：\n成绩表现：{performance}\n学习态度：积极认真\n"
            "优势：基础知识扎实\n待提升：综合应用能力\n教师寄语：{advice}",
            
            "【学情分析报告】\n学生：{name}\n学科：{subject}\n综合评级：{performance}\n"
            "详细分析：近期成绩{trend}，课堂互动{class_interaction}次/周\n个性化建议：{advice}"
        ]
        
        # 解析学生数据（简化处理）
        data = json.loads(prompt.split("学生数据：")[-1])
        
        # 根据成绩计算表现评级
        avg_score = sum(data["recent_scores"]) / len(data["recent_scores"]) if data["recent_scores"] else 0
        if avg_score >= 90:
            performance = "优秀"
            advice = "继续保持当前学习状态，可尝试挑战更高难度内容"
        elif avg_score >= 80:
            performance = "良好" 
            advice = "基础扎实，建议加强综合题型训练"
        elif avg_score >= 60:
            performance = "合格"
            advice = "需要加强薄弱环节的练习，建议每周额外练习2小时"
        else:
            performance = "待提升"
            advice = "建议安排一对一辅导，重点巩固基础知识"
        
        # 判断成绩趋势
        if len(data["recent_scores"]) >= 2:
            trend = "上升" if data["recent_scores"][-1] > data["recent_scores"][0] else "稳定" if data["recent_scores"][-1] == data["recent_scores"][0] else "下降"
        else:
            trend = "数据不足"
        
        # 选择模板并填充
        template = random.choice(report_templates)
        report = template.format(
            name=data["student_name"],
            subject=data["subject"],
            performance=performance,
            trend=trend,
            attendance=data["attendance_rate"],
            homework=data["homework_completion"],
            class_interaction=data["class_interaction"],
            advice=advice
        )
        
        return report
    
    def generate_student_data(self, student_id: str) -> Dict[str, Any]:
        """生成模拟学生数据
        
        Args:
            student_id: 学生ID
            
        Returns:
            Dict: 学生数据字典
        """
        subjects = ["数学", "语文", "英语", "物理", "化学"]
        
        data = self.student_data_template.copy()
        data["student_id"] = student_id
        data["student_name"] = f"学生{student_id[-3:]}"
        data["subject"] = random.choice(subjects)
        data["recent_scores"] = [random.randint(60, 100) for _ in range(3)]
        data["attendance_rate"] = round(random.uniform(0.85, 1.0), 2)
        data["homework_completion"] = round(random.uniform(0.7, 1.0), 2)
        data["class_interaction"] = random.randint(3, 15)
        
        return data
    
    def generate_report(self, student_id: str) -> Dict[str, Any]:
        """生成学情分析报告
        
        Args:
            student_id: 学生ID
            
        Returns:
            Dict: 包含报告信息的字典
        """
        # 1. 获取学生数据
        student_data = self.generate_student_data(student_id)
        
        # 2. 构建大模型提示词
        prompt = f"""请根据以下学生数据生成一份学情分析报告：
        要求：1. 包含成绩分析 2. 学习状态评价 3. 个性化建议
        学生数据：{json.dumps(student_data, ensure_ascii=False, indent=2)}"""
        
        # 3. 调用大模型生成报告（模拟）
        report_content = self.simulate_llm_api_call(prompt)
        
        # 4. 构建报告结果
        report = {
            "report_id": f"REPORT_{student_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "student_info": {
                "id": student_data["student_id"],
                "name": student_data["student_name"],
                "subject": student_data["subject"]
            },
            "generated_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "report_content": report_content,
            "metadata": {
                "model_used": "simulated_llm_v1.0",
                "generation_time_ms": random.randint(500, 2000)
            }
        }
        
        return report
    
    def batch_generate_reports(self, student_ids: List[str]) -> List[Dict[str, Any]]:
        """批量生成学情报告
        
        Args:
            student_ids: 学生ID列表
            
        Returns:
            List: 报告列表
        """
        reports = []
        for student_id in student_ids:
            try:
                report = self.generate_report(student_id)
                reports.append(report)
                print(f"✓ 已生成报告：{report['report_id']}")
            except Exception as e:
                print(f"✗ 生成失败 {student_id}: {str(e)}")
        
        return reports


def main():
    """主函数：智能学情报告生成系统入口"""
    print("=" * 50)
    print("智能学情分析报告生成系统")
    print("=" * 50)
    
    # 初始化报告生成器
    generator = LearningReportGenerator()
    
    # 模拟一批学生ID
    student_ids = [f"STU{1000 + i}" for i in range(5)]
    
    print(f"\n开始为 {len(student_ids)} 名学生生成学情报告...")
    print("-" * 50)
    
    # 批量生成报告
    reports = generator.batch_generate_reports(student_ids)
    
    # 输出统计结果
    print("\n" + "=" * 50)
    print("报告生成完成！")
    print(f"成功生成报告数：{len(reports)}/{len(student_ids)}")
    
    # 展示一份样例报告
    if reports:
        print("\n样例报告预览：")
        print("-" * 50)
        sample = reports[0]
        print(f"报告ID：{sample['report_id']}")
        print(f"学生：{sample['student_info']['name']} ({sample['student_info']['id']})")
        print(f"学科：{sample['student_info']['subject']}")
        print(f"生成时间：{sample['generated_time']}")
        print("\n报告内容：")
        print(sample['report_content'])
        print("-" * 50)
    
    # 模拟A/B测试数据
    print("\n模拟A/B测试结果：")
    print("原系统教师查看报告比例：45%")
    print("新系统教师查看报告比例：60.75%")
    print("提升效果：35% (通过引入大模型自动生成)")
    
    return reports


if __name__ == "__main__":
    main()