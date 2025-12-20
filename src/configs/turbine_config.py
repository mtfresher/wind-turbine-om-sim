class TurbineConfig:
    """
    风机模拟的配置参数
    """

    def __init__(self, v_in=3.0, v_rated=12.0, v_out=25.0, p_rated=2000.0,
                 noise_sigma=0.02, rpm_min=6.0, rpm_rated=15.0, rpm_noise_sigma=0.2):
        """
        :param v_in: 切入风速 (m/s)
        :param v_rated: 额定风速 (m/s)
        :param v_out: 切出风速 (m/s)
        :param p_rated: 额定功率 (kW)
        :param noise_sigma: 功率噪声比例（相对额定功率）
        :param rpm_min: 最低运行转速 (rpm)
        :param rpm_rated: 额定转速 (rpm)
        :param rpm_noise_sigma: 转速噪声 (rpm)
        """
        self.v_in = v_in
        self.v_rated = v_rated
        self.v_out = v_out
        self.p_rated = p_rated
        self.noise_sigma = noise_sigma
        self.rpm_min = rpm_min
        self.rpm_rated = rpm_rated
        self.rpm_noise_sigma = rpm_noise_sigma