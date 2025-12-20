import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetection:
    """
    风机异常检测类，使用孤立森林算法检测异常数据点。
    """

    def __init__(self, contamination=0.1):
        """
        初始化异常检测器
        :param contamination: 异常样本的比例
        """
        self.contamination = contamination
        self.model = IsolationForest(contamination=self.contamination)

    def fit(self, data):
        """
        拟合模型
        :param data: 输入数据，numpy数组
        """
        self.model.fit(data)

    def predict(self, data):
        """
        预测数据中的异常点
        :param data: 输入数据，numpy数组
        :return: 异常点的预测结果，1表示正常，-1表示异常
        """
        return self.model.predict(data)

    def detect_anomalies(self, data):
        """
        检测异常点并返回异常点的索引
        :param data: 输入数据，numpy数组
        :return: 异常点的索引
        """
        predictions = self.predict(data)
        return np.where(predictions == -1)[0]  # 返回异常点的索引

# 示例用法
if __name__ == "__main__":
    # 生成示例数据
    normal_data = np.random.normal(loc=0.0, scale=1.0, size=(100, 1))
    anomaly_data = np.random.normal(loc=5.0, scale=1.0, size=(10, 1))
    data = np.vstack((normal_data, anomaly_data))

    # 初始化异常检测器
    anomaly_detector = AnomalyDetection(contamination=0.1)
    anomaly_detector.fit(data)

    # 检测异常点
    anomalies = anomaly_detector.detect_anomalies(data)
    print("Detected anomalies at indices:", anomalies)