# 第六章理论笔记：解线性方程组的直接方法

本笔记整理第六章反复使用的定义、公式和误差指标。Notebook 会结合教学式代码和实验展开这些内容。

## 1. 线性方程组与直接方法

线性方程组写作

$$
A\boldsymbol{x}=\boldsymbol{b},
$$

其中 \(A\in\mathbb R^{n\times n}\)、\(\boldsymbol{x},\boldsymbol{b}\in\mathbb R^n\)。直接方法通过有限步消元或矩阵分解求解，例如高斯消元、LU 分解、Cholesky 分解和 QR 分解。

在精确算术下，非奇异矩阵可以通过有限步得到精确解；在浮点算术下，舍入误差、主元大小和矩阵条件数都会影响结果。因此实际计算中不能只问“解出来没有”，还要检查残差、前向误差和矩阵结构。

## 2. 前代和回代

下三角方程组

$$
L\boldsymbol{y}=\boldsymbol{b}
$$

可由前代求解：

$$
y_i=\frac{b_i-\sum_{j=1}^{i-1}l_{ij}y_j}{l_{ii}},
\qquad i=1,\ldots,n.
$$

若 \(L\) 为单位下三角矩阵，则 \(l_{ii}=1\)。

上三角方程组

$$
U\boldsymbol{x}=\boldsymbol{y}
$$

可由回代求解：

$$
x_i=\frac{y_i-\sum_{j=i+1}^{n}u_{ij}x_j}{u_{ii}},
\qquad i=n,n-1,\ldots,1.
$$

前代和回代的计算量均为 \(O(n^2)\)。多数直接法先把 \(A\) 化为三角矩阵或三角分解，再调用这两个过程。

## 3. 高斯消元

高斯消元通过初等行变换把 \(A\) 化为上三角矩阵。第 \(k\) 步中，用主元 \(a_{kk}^{(k)}\) 消去其下方元素：

$$
m_{ik}=\frac{a_{ik}^{(k)}}{a_{kk}^{(k)}},
\qquad
R_i\leftarrow R_i-m_{ik}R_k,
\qquad i=k+1,\ldots,n.
$$

消元结束后得到

$$
U\boldsymbol{x}=\widetilde{\boldsymbol{b}},
$$

再用回代求解。

不选主元的高斯消元在主元为零时会直接失败；主元很小时也会放大舍入误差。部分选主元在每一列从当前行及其下方选择绝对值最大的元素作为主元，并进行行交换。数学上可以写成

$$
PA=LU,
$$

其中 \(P\) 是置换矩阵。

一般稠密高斯消元的主要计算量为 \(O(n^3)\)，回代为 \(O(n^2)\)。当只有一个右端项时，可以直接消元；当有多个右端项时，先分解 \(A\) 再重复三角求解更划算。

## 4. LU 分解

若高斯消元过程中不发生行交换，并且所有主元非零，则可以把矩阵写成

$$
A=LU,
$$

其中 \(L\) 为下三角矩阵，\(U\) 为上三角矩阵。Doolittle 分解约定 \(L\) 的对角元为 1。

从矩阵乘法

$$
a_{ij}=\sum_{k=1}^{n}l_{ik}u_{kj}
$$

出发，可以得到递推公式：

$$
u_{ij}=a_{ij}-\sum_{k=1}^{i-1}l_{ik}u_{kj},
\qquad j=i,\ldots,n,
$$

$$
l_{ji}=\frac{a_{ji}-\sum_{k=1}^{i-1}l_{jk}u_{ki}}{u_{ii}},
\qquad j=i+1,\ldots,n.
$$

带部分选主元时，分解写为

$$
PA=LU.
$$

程序中通常不显式构造大型置换矩阵，而是用置换向量记录行交换。求解时先置换右端项：

$$
LU\boldsymbol{x}=P\boldsymbol{b}.
$$

然后求

$$
L\boldsymbol{y}=P\boldsymbol{b},
\qquad
U\boldsymbol{x}=\boldsymbol{y}.
$$

## 5. 对称正定矩阵与 Cholesky 分解

对称正定矩阵满足

$$
A=A^T,
\qquad
\boldsymbol{x}^TA\boldsymbol{x}>0
\quad(\boldsymbol{x}\ne0).
$$

这类矩阵可以做 Cholesky 分解：

$$
A=LL^T,
$$

其中 \(L\) 为下三角矩阵且对角元为正。递推公式为

$$
l_{jj}=\sqrt{a_{jj}-\sum_{k=1}^{j-1}l_{jk}^2},
$$

$$
l_{ij}=\frac{a_{ij}-\sum_{k=1}^{j-1}l_{ik}l_{jk}}{l_{jj}},
\qquad i=j+1,\ldots,n.
$$

Cholesky 只存储一个三角因子，计算量大约是一般 LU 的一半。若递推中平方根内部不为正，说明矩阵不是正定，或者已经因为舍入误差偏离正定结构。

## 6. \(LDL^T\) 分解

对称正定矩阵也可以写成

$$
A=LDL^T,
$$

其中 \(L\) 为单位下三角矩阵，\(D\) 为对角矩阵。递推公式为

$$
d_j=a_{jj}-\sum_{k=1}^{j-1}l_{jk}^2d_k,
$$

$$
l_{ij}=\frac{a_{ij}-\sum_{k=1}^{j-1}l_{ik}l_{jk}d_k}{d_j}.
$$

与 Cholesky 相比，\(LDL^T\) 不显式计算平方根。对正定矩阵，\(d_j>0\)。若 \(D\) 中出现非正元素，则正定条件被破坏。对称不定矩阵也有带主元的 \(LDL^T\) 分解，但属于后续拓展。

## 7. 三对角系统与追赶法

三对角系统写作

$$
\begin{bmatrix}
b_1 & c_1 \\
a_2 & b_2 & c_2 \\
& a_3 & b_3 & c_3 \\
& & \ddots & \ddots & \ddots \\
& & & a_n & b_n
\end{bmatrix}
\boldsymbol{x}
=
\boldsymbol{d}.
$$

普通高斯消元会破坏稠密矩阵需要 \(O(n^3)\) 的成本；但三对角矩阵消元时带宽保持不变，只需要修改主对角和右端项，因此复杂度为 \(O(n)\)，存储量也是 \(O(n)\)。

追过程可以写成

$$
c'_1=\frac{c_1}{b_1},
\qquad
d'_1=\frac{d_1}{b_1},
$$

$$
c'_i=\frac{c_i}{b_i-a_i c'_{i-1}},
\qquad
d'_i=\frac{d_i-a_i d'_{i-1}}{b_i-a_i c'_{i-1}}.
$$

赶过程为

$$
x_n=d'_n,
\qquad
x_i=d'_i-c'_i x_{i+1}.
$$

追赶法本质上是三对角结构下的 LU 分解。Doolittle 和 Crout 只是对三角因子的对角元约定不同，核心信息相同。

## 8. QR 分解

QR 分解写作

$$
A=QR,
$$

其中 \(Q\) 为正交矩阵，\(R\) 为上三角矩阵。正交矩阵满足

$$
Q^TQ=I,
$$

并保持二范数：

$$
\|Q\boldsymbol{x}\|_2=\|\boldsymbol{x}\|_2.
$$

因此 QR 分解在最小二乘和病态问题中比法方程更稳定。对方阵系统，可求

$$
R\boldsymbol{x}=Q^T\boldsymbol{b}.
$$

### Gram-Schmidt

经典 Gram-Schmidt 通过反复减去已有正交向量上的投影构造正交基：

$$
\boldsymbol{v}_j
=
\boldsymbol{a}_j-\sum_{i=1}^{j-1}
(\boldsymbol{q}_i^T\boldsymbol{a}_j)\boldsymbol{q}_i.
$$

修正 Gram-Schmidt 每次用当前剩余向量做投影，浮点运算下通常比经典形式保持更好的正交性。应使用

$$
\|Q^TQ-I\|
$$

检查正交性，而不是只看 \(QR\approx A\)。

### Householder

Householder 反射形如

$$
H=I-2\boldsymbol{v}\boldsymbol{v}^T,
\qquad \|\boldsymbol{v}\|_2=1.
$$

它可以把一个向量反射到坐标轴方向，从而一次消去一列中主元下方的所有元素。Householder QR 通常比 Gram-Schmidt 更稳定，是稠密矩阵 QR 的标准选择。

### Givens

Givens 旋转只作用在两个坐标平面上，用

$$
\begin{bmatrix}
c & s\\
-s & c
\end{bmatrix}
$$

消去一个指定元素。它适合稀疏矩阵、增量更新和只需要局部消元的场景。完整稠密矩阵上，Householder 通常更高效。

## 9. 残差、前向误差和条件数

数值解 \(\widehat{\boldsymbol{x}}\) 的残差为

$$
\boldsymbol{r}
=
\boldsymbol{b}-A\widehat{\boldsymbol{x}}.
$$

相对残差小表示方程被近似满足，但不一定说明解接近精确解。若矩阵病态，微小的右端项扰动或舍入误差也可能造成明显的前向误差。

条件数

$$
\kappa(A)=\|A\|\,\|A^{-1}\|
$$

刻画问题本身对扰动的敏感性。算法稳定性刻画算法是否额外放大误差。一个稳定算法也无法消除病态问题的固有困难；一个条件良好的问题也可能被不稳定算法算坏。

## 10. 方法选择

| 矩阵结构 | 推荐直接方法 | 主要原因 |
| --- | --- | --- |
| 一般稠密非奇异矩阵 | 部分选主元 LU / 高斯消元 | 适用范围广，稳定性较好 |
| 多个右端项 | LU 或 PLU | 分解一次，重复前代和回代 |
| 对称正定矩阵 | Cholesky 或 \(LDL^T\) | 利用对称和正定结构，计算量更低 |
| 三对角矩阵 | Thomas 追赶法 | \(O(n)\) 时间和存储 |
| 最小二乘或需要正交稳定性 | QR | 正交变换不放大二范数 |
| 稀疏或增量消元 | Givens / 稀疏直接法 | 保持局部结构，便于更新 |

实际选择算法时，应先识别矩阵结构，再考虑稳定性、规模、存储和是否有多个右端项。
