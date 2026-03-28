---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Three.js"
title: "Three.js removes Geometry class, breaking thousands of WebGL art sketches"
date: "2021-01-28"
dependency: "Three.js (WebGL library)"
event_type: "sdk-deprecation"
severity: "major"
summary: "Three.js r125, released January 28, 2021, removed the foundational THREE.Geometry class from the core library, breaking virtually every tutorial, code example, and creative WebGL project written before 2020 that loaded three.js from a CDN."
links:
  - url: "https://discourse.threejs.org/t/three-geometry-will-be-removed-from-core-with-r125/22401"
    label: "Three.js Forum: THREE.Geometry will be removed from core with r125"
  - url: "https://github.com/mrdoob/three.js/wiki/Migration-Guide"
    label: "Three.js Migration Guide"
  - url: "https://github.com/mrdoob/three.js/releases/tag/r125"
    label: "Three.js r125 Release Notes"
fixes:
  - type: migration
    description: "Replace all THREE.Geometry usage with THREE.BufferGeometry. This requires rewriting how vertices, faces, and UVs are defined — BufferGeometry uses typed arrays rather than object-oriented vertex/face classes."
  - type: workaround
    description: "Pin projects to a specific Three.js version rather than loading 'latest' from a CDN. Projects that referenced a fixed version URL are unaffected."
---

## What changed

Three.js, created by Ricardo Cabello (mrdoob), is the dominant JavaScript library for WebGL-based 3D graphics on the web. Since its creation in 2010, the THREE.Geometry class was the primary way developers defined 3D shapes — using an intuitive API of vertices, faces, and UVs stored as JavaScript objects.

In release r125 (January 28, 2021), THREE.Geometry was removed from the core and moved to a deprecated ES6 module. This was not a soft deprecation — code using `new THREE.Geometry()` would throw an error if loading the current version of three.js. The replacement, THREE.BufferGeometry, uses flat typed arrays (Float32Array) instead of object arrays, requiring a fundamentally different approach to defining geometry.

The breakage was widespread because Three.js has no semantic versioning and no LTS releases. Its release model is a rolling series of numbered releases (r1, r2, ... r125, ...) with no stability guarantees. Many creative coding projects, online tutorials, and WebGL art experiments loaded Three.js from CDN URLs pointing to "latest" or unversioned paths. When r125 went live, these projects silently broke.

The Three.js community forum thread announcing the removal drew extensive discussion from developers whose projects broke. The SubdivisionModifier was also removed in the same release, compounding the damage for projects that used both features.

## Notes

Three.js's rapid release cadence (roughly monthly) and lack of semantic versioning makes it uniquely dangerous for unmaintained web art. The project's own migration guide recommends incremental upgrades (e.g., r70 to r80 to r90) rather than jumping across many versions — advice that is irrelevant for abandoned creative works. A WebGL art piece from 2015 that loads three.js from a CDN may silently break on any given month when a new release deprecates an API it depends on.
