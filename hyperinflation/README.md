# Hyperinflation Calculations

## Index
- Background and Goal
- Assumptions From References
- Exponential Expansion Model
- Duration and Number of Doublings
- Radius Growth Check
- How We Use It In The Brane Model
- Hubble-Based Size Estimate (Center vs Edge) for 2026-01-01

## Background and Goal
In this TOE model, two primordial universes collide: the protonmos (proton universe)
and the electronmos (electron universe). Their collision forms the cosmos, and the
expansion of the contact region is interpreted as "inflation" in this context.

The goal of these calculations is to translate expansion data into estimates for
contact growth, relative velocities, and (later) approximate radii and masses for
the original protonmos/electronmos.

This note summarizes the inflation-speed estimates used for our brane collision
model and shows the math that converts "doubling time" to a growth rate.

## Assumptions From References
- Distances doubled every ~1e-37 s during inflation.
- Inflation lasted at least ~1e-35 s.
- Radius grew from ~4e-29 m to ~0.9 m by the end of inflation (order-of-magnitude).

Source: https://en.wikipedia.org/wiki/Cosmic_inflation

## Exponential Expansion Model
Let a(t) be the scale factor of space. If distances double every td seconds:
  a(t) = a0 * 2^(t / td)

This is equivalent to:
  a(t) = a0 * exp(H * t)
  H = ln(2) / td

With td = 1e-37 s:
  H ~= 0.693 / 1e-37 ~= 6.93e36 s^-1

## Duration and Number of Doublings
If inflation lasts T = 1e-35 s:
  N = T / td = 1e-35 / 1e-37 = 100 doublings
  Growth factor = 2^100 ~= 1.27e30
  E-folds = N * ln(2) ~= 69.3

## Radius Growth Check
From 4e-29 m to 0.9 m:
  Factor ~= 0.9 / 4e-29 ~= 2.25e28
  E-folds ~= ln(2.25e28) ~= 65

This is consistent with the 60-70 e-fold range often cited.

## How We Use It In The Brane Model
Two possible interpretations for the animation:
1) Treat separation between branes as exponential in time:
   d(t) = d0 * exp(H * t)
2) Keep brane motion linear but scale the "space" textures by a(t).

We can pick either depending on the visual and physical narrative.

## Hubble-Based Size Estimate (Center vs Edge) for 2026-01-01
Assume the "current size" equals the observable-universe radius:
  R_today ~= 46.5 Gly ~= 4.4e26 m

We model two expansion rates:
- Center (Hubble/Planck): H0 ~= 67.4 km/s/Mpc
- Edge (faster, local):   H0 ~= 73.0 km/s/Mpc

Convert H0 to s^-1:
  1 Mpc ~= 3.0857e19 km
  H0_center ~= 2.19e-18 s^-1
  H0_edge   ~= 2.37e-18 s^-1

Over 1 year (dt ~= 3.15576e7 s):
  frac_center ~= H0_center * dt ~= 6.9e-11
  frac_edge   ~= H0_edge * dt   ~= 7.5e-11
  frac_avg    ~= 7.2e-11

So the radius increase over 1 year is:
  dR_center ~= R_today * 6.9e-11 ~= 3.0e16 m
  dR_edge   ~= R_today * 7.5e-11 ~= 3.3e16 m
  dR_avg    ~= R_today * 7.2e-11 ~= 3.2e16 m

Interpretation in the brane model:
- Use H0_center for the slower core region.
- Use H0_edge for the faster rim region.
- Use the average as a single global growth rate if needed.
