# PyAnaSolution

## Introduction
PyAnaSolution is a comprehensive package that includes analytical solution programs for benchmark test cases widely 
utilized in numerical simulation algorithm research.
Our objective is to provide a resource that spares new researchers in the field from the time-consuming process of 
understanding analytical solution calculations.

This package encompasses analytical solutions for various scenarios, including:

* Convection Diffusion Equation (CDE)
  * Channel Cos Flow
  * Gaussian Hill
  * Poiseuille Flow
  * Semi Infinite Flow (1D)
  * Uniform Flow
* Geothermal Analysis
  * Fracture Thermal Flow
  * Reinjection (1D)
  * Reinjection (2D)
* Hydrology Studies
  * Theis

Example programs for each analytical solution can be found in the 'examples' directory.

We are committed to continually enhancing this library and encourage contributions of new analytical solution programs.


## Installation Guide
To install PyAnaSolution for the first time, use the following command:
```
pip install pyanasolution
```
To update PyAnaSolution to the latest version, run:
```
pip install --upgrade pyanasolution
```

## Analytical solutions

To obtain settable parameters for the calculation of analytical solutions, a universal approach is to call the 'doc'
method of the analytical solution class. For instance, to understand the parameters of the Theis solution, you can use
the following code:

```python
import pyanasolution as pas

theis = pas.Theis()
theis.doc()
```

```
[PyAnaSolution - Theis]
 * The Theis model is a seminal mathematical solution in the field of hydrogeology for quantifying transient groundwater flow in a confined aquifer. (Provided by ChatGPT)
[Parameters]
 * ----------------------|---------|---------|--------------------|------------------------------------------------|
 *  PARAMETERS NAME      | UNIT    | VALUE   | TYPE               | INTRODUCTION                                   |
 * ----------------------|---------|---------|--------------------|------------------------------------------------|
 *  Flow rate            | m^3/s   | 0       | float              | The injection well is positive and vice versa. |
 *  Gravity acceleration | m/(s^2) | 9.8     | float              | The gravity acceleration.                      |
 *  Initial head         | m       | 0       | float              | The initial head of the field.                 |
 *  Permeability         | m^2     | 0       | float              |                                                |
 *  Storage              | m^(-1)  | 0       | float              |                                                |
 *  Thick                | m       | 1       | float              | The aquifer thick.                             |
 *  Time                 | s       | 0       | float              | The operation time.                            |
 *  Fluid density        | kg/m^3  | 1000    | float              |                                                |
 *  Fluid viscosity      | Pa∙s    | 0.00101 | float              |                                                |
 *  Well coordinate      | m       | [0. 0.] | list or np.ndarray |                                                |
 * ----------------------|---------|---------|--------------------|------------------------------------------------|
```

### Covection Diffusion Equation (CDE)

The standard convection diffusion equation (CDE) is given as:

$$ 
\frac{\partial \phi}{\partial t}+\nabla\cdot\left(\boldsymbol{v}\phi\right)=
\nabla\cdot\left(\boldsymbol{D}\nabla\phi\right)+q
$$

or written in another form:

$$
\frac{\partial \phi}{\partial t}+u\frac{\partial \phi}{\partial x}+v\frac{\partial \phi}{\partial y}+
w\frac{\partial \phi}{\partial z}=D_{xx}\frac{\partial^2 \phi}{\partial x^2}+D_{yy}\frac{\partial^2 \phi}{\partial y^2}
+D_{zz}\frac{\partial^2 \phi}{\partial z^2}+q
$$

where $\phi$ is a general scalar variable, t is the time and $\boldsymbol{D}$ is the diffusion coefficient.

#### 1. Channel Cos Flow

![Channel Cos Flow](resources/images/channel_cos_flow_contour.jpg)


#### 2. Gaussian Hill

![Gaussian Hill](resources/images/gaussian_hill_contour.jpg)

#### 3. Poiseuille Flow

![Poiseuille Flow](resources/images/poiseuille_flow_contour.jpeg)

#### 4. Semi Infinite Flow (1D)

Conditions:

* $\phi\left(x, 0\right) = 0$
* $\phi\left(0, t\right) = 1$
* $\phi\left(\infty, t\right) = 0$

Solution:

$$
\phi(x, t)=\frac{1}{2}\left[\operatorname{erfc}\left(\frac{x-v t}{2 \sqrt{D t}}\right)+e^{(v x / D)} \operatorname{erfc}
\left(\frac{x+v t}{2 \sqrt{D t}}\right)\right]
$$

Example:

* $v=70$
* $D=20$
* $t\in\left(0, 1\right)$

![Semi Infinite Flow 1D](resources/images/semi_infinite_flow_1d.gif)

Reference:

[1] F. Wang, W. Chen, A. Tadeu, and C. G. Correia, “Singular boundary method for transient convection–diffusion problems
with time-dependent fundamental solution,” Int. J. Heat Mass Transfer, vol. 114, pp. 1126–1134, Nov. 2017,
doi: 10.1016/j.ijheatmasstransfer.2017.07.007.


#### 4. Uniform Flow

![Uniform Flow](resources/images/uniform_flow_contour.jpeg)

### Geothermal Analysis

#### 1. Fracture Thermal Flow

![Fracture Thermal Flow](resources/images/fracture_thermal_flow_contour.jpeg)

#### 2. Reinjection (1D)

![Reinjection 1D](resources/images/reinjection_1d_contour.jpg)

#### 3. Reinjection (2D)

![Reinjection 2D](resources/images/reinjection_2d_contour.jpg)

### Hydrology Studies
#### 1. Theis

![Theis](resources/images/theis_contour.jpg)

## Contact Us
For any inquires, please contact us at frankhp921@163.com.