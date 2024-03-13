import json
import os
import shutil
from collections import namedtuple
from typing import List, Sequence, Dict

from ..io.config import Properties
from os import PathLike


class ReportHelper:
    __data: dict
    """
    {
  "allure_result_path": "allure-result",
  "allure_report_path": "allure-report",
  "allure_history_source_path": "allure-report/history",
  "allure_history_target_path": "allure-result/history",
  "allure_host": "127.0.0.1",
  "allure_port": "8081",
  "allure_link_pattern": "issue:https://github.com/allure-framework/allure-python/issues/{}"
}
    """

    @classmethod
    def load_from_json_object(cls, data: dict) -> "ReportHelper":
        if not isinstance(data, dict):
            raise ValueError("error format json object")
        helper = ReportHelper()
        helper.__data = data
        return helper

    @classmethod
    def load_from_json(cls, json_str: str) -> "ReportHelper":
        data = json.loads(json_str)
        if not isinstance(data, dict):
            raise ValueError("error format json")
        helper = ReportHelper()
        helper.__data = data
        return helper

    @classmethod
    def load_from_file(cls, json_file: str | PathLike) -> "ReportHelper":
        with open(json_file, "rt", encoding="utf-8", newline=None) as f:
            data = f.read()
        return cls.load_from_json(data)

    @property
    def allure_result_path(self) -> str:
        return self.__data.get("allure_result_path", "")

    @property
    def allure_report_path(self) -> str:
        return self.__data.get("allure_report_path", "")

    @property
    def allure_history_source_path(self) -> str:
        report_path = self.allure_report_path
        if not report_path:
            return ""
        return f"{report_path}/history"

    @property
    def allure_history_target_path(self) -> str:
        result_path = self.allure_result_path
        if not result_path:
            return ""
        return f"{result_path}/history"

    @property
    def allure_host(self) -> str:
        return self.__data.get("allure_host", "")

    @property
    def allure_port(self) -> str:
        return self.__data.get("allure_port", "")

    @property
    def allure_link_pattern(self) -> Sequence[str]:
        return self.__data.get("allure_link_pattern", [])

    @property
    def allure_summary_path(self) -> str:
        result_path = self.allure_result_path
        if not result_path:
            return ""
        return f"{result_path}/widgets/summary.json"

    @staticmethod
    def run_command(c: str):
        error_gene = os.popen(c)
        # 读下内容，防止阻塞异步执行
        error_content = error_gene.read()
        exit_code = error_gene.close()
        if exit_code:
            raise Exception(error_content)

    def make_property_file(self, source: str, **kwargs):
        """
        加载source指定的environment.properties文件，并将kwargs指定的内容更新进去。将结果文件写到allure_result_path中去

        :param source: source的文件可以不存在。
        :param kwargs:
        :return:
        """

        # 支持下environment.properties不存在清空
        if not os.path.exists(source):
            p = Properties.load_from_str([])
        else:
            p = Properties.load_from_file(source)
        result_path_property = os.path.join(self.allure_result_path, "environment.properties")

        # 加一些自定义的变量
        if kwargs:
            p.update(kwargs)
        p.write_file(result_path_property)

    def make_category(self, source: str):
        """
        如果源文件存在就把文件复制到allure_result_path,并改名为categories.json
        :param source:
        :return:
        """
        if os.path.exists(source):
            result_path_category = os.path.join(self.allure_result_path, "categories.json")
            shutil.copy(source, result_path_category)

    def make_history(self):
        """
        将allure_history_source_path中history目录拷贝allure_history_target_path。如果之前存在allure_history_target_path，先删除
        :return:
        """
        # 清空report目录前先拷贝
        if os.path.exists(self.allure_history_source_path):
            # 做下兜底，如果没有指定--clean-alluredir,allure_history_target_path就会存在
            if os.path.exists(self.allure_history_target_path):
                shutil.rmtree(self.allure_history_target_path)
            shutil.copytree(self.allure_history_source_path, self.allure_history_target_path)

    def generate_report(self):
        """
        确保你的allure在path中。将报告生成到allure_report_path
        :param source:
        :param kwargs:
        :return:
        """
        command_gene = f"allure generate -c -o {self.allure_report_path} {self.allure_result_path}"
        self.run_command(command_gene)

    def open_report(self):
        """
        确保你的allure在path中
        :param source:
        :param kwargs:
        :return:
        """
        command_open = f"allure open --host {self.allure_host} --port {self.allure_port} {self.allure_report_path}"
        self.run_command(command_open)

    def report_summary(self) -> Dict[str, str]:
        """
        total  总用例
        passed   通过
        failed  失败
        skipped    跳过
        run_time 时间
        min_time  最小单用例运行时间
        max_time  最大单用例运行时间
        :return:
        """
        with open(self.allure_summary_path, 'rt', encoding="utf-8") as f:
            data = json.loads(f.read())
        return dict(
            total=data['statistic']['total'],  # 总用例
            passed=data['statistic']['passed'],  # 通过
            failed=data['statistic']['failed'],  # 失败
            skipped=data['statistic']['skipped'],  # 跳过
            run_time=data['time']['duration'],  # 时间
            min_time=data['time']['minDuration'],  # 最小单用例运行时间
            max_time=data['time']['maxDuration']  # 最大单用例运行时间
        )
