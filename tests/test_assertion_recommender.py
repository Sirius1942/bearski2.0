"""测试智能断言推荐模块"""
from core.assertion_recommender import AssertionRecommender


def test_api_response_analysis():
    """测试 API 响应分析"""
    # 模拟 API 响应
    response = {
        'status_code': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': {
            'code': 0,
            'success': True,
            'message': '操作成功',
            'data': {
                'user_id': 12345,
                'username': 'test_user'
            }
        },
        'duration': 250
    }
    
    # 分析响应
    recommendations = AssertionRecommender.analyze_response(response)
    
    print(f"\n✅ 分析完成，生成 {len(recommendations)} 条断言推荐：\n")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. [{rec['type']}] {rec['reason']}")
        print(f"   {rec['assertion']}\n")
    
    # 生成测试代码
    test_code = AssertionRecommender.generate_test_code('user_info', response)
    print("\n📝 生成的测试代码：")
    print("=" * 60)
    print(test_code)
    print("=" * 60)
    
    # 保存推荐结果
    AssertionRecommender.save_recommendations(recommendations, 'recommendations.json')
    print("\n💾 推荐结果已保存到 recommendations.json")


if __name__ == '__main__':
    test_api_response_analysis()
