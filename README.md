# Garden

An automated garden system built as an experiment at the intersection of agentic AI and physical computing.

## What is this?

This project is a personal learning experiment combining two interests:

1. **Agentic AI** - Exploring how AI agents can reason about and interact with the physical world
2. **Raspberry Pi & Sensors** - Getting hands dirty with hardware, sensors, and real-world data

The goal is to build a system that can monitor environmental conditions (temperature, humidity, soil moisture, light) and make autonomous decisions about plant care - when to water, when to turn on grow lights, when to adjust ventilation.

## The Idea

Plants are surprisingly complex systems. They respond to dozens of environmental factors, and keeping them happy requires constant attention to conditions that change throughout the day. This project aims to:

- **Observe** - Collect continuous data from environmental sensors
- **Understand** - Transform noisy sensor readings into meaningful state (Is the soil drying out? Is the climate trending warmer?)
- **Act** - Use an AI agent to make decisions about actuators (pumps, lights, fans) based on derived state

The interesting part isn't the automation itself - simple threshold-based systems have existed forever. The interesting part is using agentic AI as the control system. Instead of hardcoded rules, an AI agent reasons about the current state and decides what actions to take. This is an exploration of what it looks like to put an AI agent in charge of a real physical system with real consequences.

## Status

Work in progress. The scaffolding and core abstractions are in place. Currently focused on the state derivation layer.

## Hardware

Built for Raspberry Pi with common garden automation sensors (DHT22 for climate, soil moisture probes, photoresistors for light detection) and actuators (relay-controlled pumps, lights, and fans).

## License

This is a personal experiment. Feel free to look around and borrow ideas.
