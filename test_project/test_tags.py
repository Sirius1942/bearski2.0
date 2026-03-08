from core.tag_manager import TagManager

# 创建标签管理器
tm = TagManager()

# 添加标签
tm.add_tag("test_login", "smoke")
tm.add_tag("test_login", "critical")
tm.add_tag("test_register", "smoke")
tm.add_tag("test_payment", "critical")
tm.add_tag("test_payment", "integration")
tm.add_tag("test_search", "ui")

# 查询标签
print("test_login 标签:", tm.get_tags("test_login"))
print("\n所有标签:", tm.get_all_tags())
print("\n标签统计:", tm.get_tag_stats())

# 筛选测试用例
print("\nsmoke 测试:", tm.filter_by_tag("smoke"))
print("critical 测试:", tm.filter_by_tag("critical"))
print("smoke 或 ui:", tm.filter_by_tags(["smoke", "ui"], match_all=False))
print("smoke 且 critical:", tm.filter_by_tags(["smoke", "critical"], match_all=True))
