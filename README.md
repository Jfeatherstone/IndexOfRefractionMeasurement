## Index of Refraction Measurement Setup

This repo includes a collection of tools in Python to measure the index of refraction of a material as described in [1].We are using the following pieces of equipment:

- *ESP301 Newport Motion Controller*: For controlling the rotation stage precisely
- *Thorlabs Beam Profiler BP209-VIS/M*: For measuring the center of the beam (as opposed to the knife edge technique)

I have written two custom libraries to interface with these devices in Python, which can be found in the `ESP301Control` and `TLBP2Control` directories respectively. These are also available in their own repos, including more information about how to utilize them/how they are constructed.

The basic idea of the experiment is to measure the displacement of a laser as a function of it's incident angle on a sample.

(Image from Nemoto (1992)

[figure 4, Nemoto 1992](images/nemoto_1992_fig_4.PNG)

### Usage

I would highly recommend using the initialization walkthrough when setting up the experiment:

```
python Initialization.py
```

This will check whether all of the proper libraries are installed, if all of the instruments are working correctly, and give advice on how to rectify any issues.

### References

[1] Nemoto 1992
