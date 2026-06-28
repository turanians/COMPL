🌌 3D Young's Double Slit Experiment Simulation 

This project is a software that simulates Young's Double Slit Experiment, one of the fundamental building blocks of quantum mechanics and wave optics, in a three-dimensional (3D) environment. Unlike traditional 2D representations, it visualizes wave interference, phase differences, and the physics of an inclined screen in a dynamic 

 Examine the relationship between wave sources, slits, and the observation screen in a 3D space.

Analysis: Observe distortions and changes in diffraction and interference patterns based on the tilt angle of the screen.Dynamic Parameters: Manipulate critical physical variables such as wavelength, distance between slits, and screen distance in real time.Multi-Platform Support:Python (VPython / PyQt5) infrastructure for desktop analysis.Three.js integration for web-based access.

  The project is developed using the following technologies to achieve high-performance 3D rendering on both desktop and web platforms:Python 3.xVPython / PyQt5 (Desktop 3D Graphics & GUI)Three.js / JavaScript (Web-based 3D Modeling)HTML5 & CSS3


Interference pattern calculations in the simulation are based on classical wave mechanics formulas, relying on the wave characteristics of light and the path difference:Path Difference: The difference in distance from the slits to any given point on the screen.Interference Conditions:Bright Fringes (Maxima): d * sin(theta) = m * lambdaDark Fringes (Minima): d * sin(theta) = (m + 1/2) * lambdaIn the case of an inclined screen, the actual 3D distance from each pixel to the wave sources is dynamically calculated using the screen's rotation 

This project is licensed under the MIT License.
