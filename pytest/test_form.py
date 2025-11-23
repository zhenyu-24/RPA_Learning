import pytest


class FormFiller:
    def fill_form(self, form_data):
        """实际的表单填写逻辑"""
        print(f"填写表单: {form_data['form_name']}")
        # 这里替换为您的实际代码
        return form_data['expected_result'] == 'success'


def get_test_cases():
    """获取测试用例数据"""
    return [
        {'test_id': 1, 'form_name': '登录表单', 'username': 'user1', 'expected_result': 'success'},
        {'test_id': 2, 'form_name': '登录表单', 'username': 'user2', 'expected_result': 'success'},
        {'test_id': 3, 'form_name': '注册表单', 'username': '', 'expected_result': 'failure'},
    ]


class TestForms:
    @pytest.fixture
    def form_filler(self):
        return FormFiller()

    # 正确写法：直接传递测试数据
    @pytest.mark.parametrize(
        "test_case",
        get_test_cases(),  # 直接传递数据列表
        ids=lambda case: f"id_{case['test_id']}_{case['form_name']}"  # 可读的测试名称
    )
    def test_form_filling(self, form_filler, test_case):
        """测试表单填写"""
        success = form_filler.fill_form(test_case)
        expected = test_case['expected_result'] == 'success'

        assert success == expected, f"用例 {test_case['test_id']} 失败"
        print(f"✅ 用例 {test_case['test_id']} 通过")