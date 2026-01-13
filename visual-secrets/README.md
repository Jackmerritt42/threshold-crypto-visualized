AI GEN
# Visual Secrets: Threshold Cryptography

A visual storytelling project using Manim to explain Shamir's Secret Sharing.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt

(AI GEN disclosures)

Technical Disclosures and Simplifications

This project is an educational visualization tool designed to build intuition for Threshold Cryptography (specifically Shamir's Secret Sharing). To make the concepts visually accessible, several mathematical simplifications were made that differ from production-grade cryptographic implementations.
1. Real Numbers vs. Finite Fields

The primary abstraction in this visualization is the use of Real Numbers (R) instead of Finite Fields (Fp​).

    In this Visual: We plot curves using continuous real numbers (decimals). This creates smooth, recognizable shapes like lines and parabolas that allow the human eye to see the relationship between points.

    In Production: Shamir's Secret Sharing operates over Finite Fields (Modular Arithmetic). This prevents information leakage through geometric analysis. If we plotted a real SSS polynomial, it would look like a scattered cloud of random noise, not a smooth curve.

2. Floating Point Precision

This code uses standard floating-point arithmetic for coordinate calculation.

    In this Visual: Reconstructions are approximate due to standard floating-point rounding errors.

    In Production: Cryptography requires exact precision. Implementations use large integers and modular inverse operations to ensure zero loss of precision during the division steps of Lagrange Interpolation.

3. Cryptographic Randomness

The randomness used in this simulation is for display purposes only.

    In this Visual: Coefficients are chosen to ensure the curve fits neatly within the 1920×1080 frame and does not shoot off to infinity.

    In Production: Coefficients must be generated using a Cryptographically Secure Pseudo-Random Number Generator (CSPRNG) and must be uniformly distributed across the entire field size. Restricting coefficients for visual constraints would introduce severe security vulnerabilities in a real system.

4. Implementation Warning

DO NOT USE THIS CODE FOR SECURITY. This repository contains drawing logic, not cryptographic logic. It is not constant-time, it is not side-channel resistant, and it does not handle private memory securely. Use standard libraries (like k256 or vault) for actual key management.