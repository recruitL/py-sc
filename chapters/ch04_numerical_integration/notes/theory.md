# 第四章理论笔记：数值积分

本笔记整理第四章中反复使用的定义、公式和误差关系。Notebook 会以实验和教学式代码展开这些内容；本文件用于集中回顾理论主线。

## 1. 求积公式

一维积分

$$
I(f)=\int_a^b f(x)\,dx
$$

的数值求积公式通常写成

$$
Q(f)=\sum_{i=0}^n w_i f(x_i),
$$

其中 \(x_i\) 是求积节点，\(w_i\) 是求积权重。若节点和权重已经包含区间长度，则 \(w_i\) 具有长度量纲；若先在标准区间构造权重，再映射到 \([a,b]\)，则还需要乘以区间变换的 Jacobian。

求积误差为

$$
E(f)=I(f)-Q(f).
$$

设计求积公式时通常同时考虑：

* 代数精度；
* 误差阶；
* 函数计算次数；
* 权重符号与稳定性；
* 被积函数的光滑性和局部变化。

## 2. 插值型求积

给定节点 \(x_0,\ldots,x_n\)，用 Lagrange 插值多项式

$$
p_n(x)=\sum_{i=0}^n f(x_i)\ell_i(x)
$$

近似 \(f(x)\)。把 \(p_n\) 积分得到

$$
\int_a^b f(x)\,dx
\approx
\int_a^b p_n(x)\,dx
=
\sum_{i=0}^n f(x_i)\int_a^b \ell_i(x)\,dx.
$$

因此插值型求积公式的权重为

$$
w_i=\int_a^b \ell_i(x)\,dx.
$$

如果求积公式对所有次数不超过 \(m\) 的多项式都精确，则称它的代数精度至少为 \(m\)。插值型公式至少具有 \(n\) 次代数精度，但由于节点对称等原因，某些公式会具有更高代数精度。例如 Simpson 公式使用三个节点，却能精确积分三次多项式。

## 3. Newton-Cotes 公式

Newton-Cotes 公式使用等距节点。若包含端点，称为闭型公式；若不包含端点，称为开型公式。

典型闭型公式包括：

中点公式：

$$
\int_a^b f(x)\,dx
\approx
(b-a) f\left(\frac{a+b}{2}\right).
$$

梯形公式：

$$
\int_a^b f(x)\,dx
\approx
\frac{b-a}{2}\left[f(a)+f(b)\right].
$$

Simpson 公式：

$$
\int_a^b f(x)\,dx
\approx
\frac{b-a}{6}\left[
f(a)+4f\left(\frac{a+b}{2}\right)+f(b)
\right].
$$

Simpson 3/8 公式：

$$
\int_a^b f(x)\,dx
\approx
\frac{3h}{8}
\left[f(a)+3f(a+h)+3f(a+2h)+f(b)\right],
\qquad h=\frac{b-a}{3}.
$$

在足够光滑的条件下，单区间误差典型形式为：

$$
E_T(f)=-\frac{(b-a)^3}{12}f''(\xi),
$$

$$
E_S(f)=-\frac{(b-a)^5}{2880}f^{(4)}(\xi).
$$

高阶 Newton-Cotes 公式并不总是更好。节点数增大后，权重可能出现较大的正负交替，对舍入误差和函数扰动更加敏感。因此实际计算中更常用低阶公式的复合形式。

## 4. 复合求积

把 \([a,b]\) 划分为 \(n\) 个小区间，步长

$$
h=\frac{b-a}{n}.
$$

复合梯形公式为

$$
T_n
=h\left[
\frac{1}{2}f(x_0)+
\sum_{i=1}^{n-1} f(x_i)
+\frac{1}{2}f(x_n)
\right].
$$

当 \(f\in C^2[a,b]\) 时，全局误差为

$$
I(f)-T_n=O(h^2).
$$

复合 Simpson 公式要求 \(n\) 为偶数：

$$
S_n
=\frac{h}{3}
\left[
f(x_0)+f(x_n)
+4\sum_{i=1,3,\ldots,n-1} f(x_i)
+2\sum_{i=2,4,\ldots,n-2} f(x_i)
\right].
$$

当 \(f\in C^4[a,b]\) 时，全局误差为

$$
I(f)-S_n=O(h^4).
$$

收敛阶可以通过步长减半实验估计：

$$
p \approx
\frac{\log(e_h/e_{h/2})}{\log 2}.
$$

## 5. Richardson 外推与 Romberg 求积

若一个近似公式满足

$$
A(h)=I+c_1h^p+c_2h^{p+q}+\cdots,
$$

则可以用两个步长的结果消去主误差项：

$$
I \approx
\frac{2^p A(h/2)-A(h)}{2^p-1}.
$$

复合梯形公式的误差展开只含偶次幂：

$$
T(h)=I+c_1h^2+c_2h^4+c_3h^6+\cdots.
$$

Romberg 求积表定义为

$$
R_{k,0}=T(h_k),\qquad h_k=\frac{b-a}{2^k},
$$

并递推

$$
R_{k,j}
=
R_{k,j-1}
+
\frac{R_{k,j-1}-R_{k-1,j-1}}{4^j-1},
\qquad j=1,\ldots,k.
$$

对光滑函数，表格对角线往往快速收敛。对不光滑、奇异或噪声函数，外推可能放大不稳定性。

## 6. 自适应 Simpson

在区间 \([a,b]\) 上记 Simpson 近似为 \(S(a,b)\)。把区间二分后得到

$$
S(a,m)+S(m,b),\qquad m=\frac{a+b}{2}.
$$

二者之差可用于估计局部误差：

$$
\epsilon
\approx
\frac{|S(a,m)+S(m,b)-S(a,b)|}{15}.
$$

若 \(\epsilon\le \text{tol}\)，接受该区间；否则递归细分。实际实现中应注意：

* 复用已经计算过的函数值；
* 把总容差分配到左右子区间；
* 设置最大递归深度；
* 在达到最大深度仍不满足容差时报告未完全收敛；
* 记录接受区间，便于观察算法把节点集中到哪里。

## 7. 高斯型求积

考虑带权积分

$$
I(f)=\int_a^b f(x)w(x)\,dx.
$$

若 \(\{p_k\}\) 是权函数 \(w(x)\) 下的正交多项式序列，则 \(n\) 点 Gauss 求积取 \(p_n\) 的 \(n\) 个零点为节点，可以达到

$$
2n-1
$$

次代数精度。

常见公式：

| 方法 | 积分区间 | 权函数 |
| --- | --- | --- |
| Gauss-Legendre | \([-1,1]\) | \(1\) |
| Gauss-Chebyshev | \([-1,1]\) | \((1-x^2)^{-1/2}\) |
| Gauss-Laguerre | \([0,\infty)\) | \(e^{-x}\) |
| Gauss-Hermite | \((-\infty,\infty)\) | \(e^{-x^2}\) |

一般区间 \([a,b]\) 上的 Gauss-Legendre 求积通过线性变换

$$
x=\frac{a+b}{2}+\frac{b-a}{2}t
$$

得到

$$
\int_a^b f(x)\,dx
=
\frac{b-a}{2}
\int_{-1}^{1}
f\left(\frac{a+b}{2}+\frac{b-a}{2}t\right)\,dt.
$$

## 8. 离散数据积分

当只给出离散样本 \((x_i,y_i)\) 时，不能自由选择求积节点，也不能无限制调用 \(f(x)\)。常见策略是先在相邻节点上构造局部插值函数，再把插值函数积分。

梯形积分：

$$
\int_{x_0}^{x_n} f(x)\,dx
\approx
\sum_{i=0}^{n-1}
\frac{y_i+y_{i+1}}{2}(x_{i+1}-x_i).
$$

局部二次积分使用三点二次插值，适合等距复合 Simpson，也能自然推广到非等距三点面板。

样条积分先构造分段三次样条

$$
s_i(x)=a_i+b_i(x-x_i)+c_i(x-x_i)^2+d_i(x-x_i)^3,
$$

再逐段积分：

$$
\int_{x_i}^{x_{i+1}} s_i(x)\,dx
=
a_i h_i+\frac{b_i}{2}h_i^2+\frac{c_i}{3}h_i^3+\frac{d_i}{4}h_i^4.
$$

含噪声数据中，高阶插值并不一定提高积分质量；平滑、采样密度和误差模型同样重要。

## 9. 多重积分

矩形区域上的二维积分可写为

$$
\int_{a}^{b}\int_{c}^{d} f(x,y)\,dy\,dx.
$$

若一维求积公式为

$$
\int_a^b g(x)\,dx\approx \sum_i w_i g(x_i),
$$

则张量积求积为

$$
\int_a^b\int_c^d f(x,y)\,dy\,dx
\approx
\sum_i\sum_j w_i v_j f(x_i,y_j).
$$

维数为 \(d\) 时，若每个方向使用 \(n\) 个节点，则总节点数为 \(n^d\)。这是高维确定性求积的主要困难。

一般区域可通过变限积分或坐标变换处理。坐标变换需要乘以 Jacobian：

$$
\int_{\Omega} f(x,y)\,dx\,dy
=
\int_{\hat\Omega}
f(x(u,v),y(u,v))
\left|\frac{\partial(x,y)}{\partial(u,v)}\right|
\,du\,dv.
$$

## 10. Monte Carlo 积分

若 \(X\) 在区域 \(\Omega\) 上均匀分布，体积为 \(|\Omega|\)，则

$$
\int_{\Omega} f(x)\,dx
=
|\Omega|\,\mathbb E[f(X)].
$$

用独立样本 \(X_1,\ldots,X_N\) 估计：

$$
\hat I_N
=
|\Omega|\frac{1}{N}\sum_{i=1}^{N} f(X_i).
$$

估计量标准误差为

$$
\operatorname{SE}(\hat I_N)
\approx
|\Omega|\sqrt{\frac{s^2}{N}},
$$

其中 \(s^2\) 是样本方差。Monte Carlo 误差通常按 \(O(N^{-1/2})\) 收敛，这个阶数慢于低维光滑函数上的高阶确定性求积，但它对维数不显式指数依赖，因此在高维问题中很重要。

一般区域可以在外接矩形中采样，并用指示函数 \(\mathbf 1_\Omega(x)\) 写成

$$
\int_{\Omega} f(x)\,dx
=
\int_B f(x)\mathbf 1_\Omega(x)\,dx.
$$

拟 Monte Carlo 用低差异序列替代伪随机样本，是后续扩展主题。
