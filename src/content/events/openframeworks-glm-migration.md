---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/OpenFrameworks"
title: "openFrameworks 0.10 replaces vector math library, breaking addon ecosystem"
date: "2018-05-07"
dependency: "openFrameworks (C++ creative coding toolkit)"
event_type: "sdk-deprecation"
severity: "major"
summary: "openFrameworks 0.10.0, released May 7, 2018, replaced the custom ofVec/ofMatrix math classes with GLM as the default vector math library, breaking compatibility with hundreds of community addons and reversing the multiplication order for matrix operations."
links:
  - url: "https://openframeworks.cc/learning/02_graphics/how_to_use_glm/"
    label: "openFrameworks: The new GLM syntax"
  - url: "https://github.com/openframeworks/openFrameworks/issues/5440"
    label: "GitHub: GLM migration and backward-compatibility strategies"
  - url: "https://forum.openframeworks.cc/t/glm-vec3-and-ofvec3f-conflict/37290"
    label: "openFrameworks Forum: glm::vec3 and ofVec3f conflict"
  - url: "https://github.com/openframeworks/openFrameworks/blob/master/CHANGELOG.md"
    label: "openFrameworks CHANGELOG"
fixes:
  - type: migration
    description: "Replace ofVec3f with glm::vec3 and reverse matrix multiplication order (ofVec used row-major v*M*V*P; GLM uses column-major P*V*M*v). The old ofVec classes still compile but are deprecated."
  - type: workaround
    description: "The old ofVec classes remain available for backward compatibility, but addons that accept ofVec3f while the core returns glm::vec3 require explicit casts or wrapper code."
---

## What changed

openFrameworks (oF) is an open-source C++ toolkit widely used for creative coding, interactive installations, and media art. Since its earliest versions, oF provided its own vector and matrix math classes — ofVec2f, ofVec3f, ofVec4f, ofMatrix3x3, ofMatrix4x4 — that formed the backbone of every geometry operation in the framework and its addon ecosystem.

In version 0.10.0 (May 7, 2018), oF replaced these custom classes with the GLM library (OpenGL Mathematics), a header-only C++ mathematics library. The core API was updated so that functions like ofNode::getPosition() return glm::vec3 instead of ofVec3f.

The most subtle and dangerous change was the reversal of matrix multiplication order. With ofVec classes, developers wrote `v * model * view * projection` (row-vector convention). With GLM, the correct order is `projection * view * model * v` (column-vector convention). Code that compiled without errors would produce silently wrong results — geometry appearing in the wrong position, cameras pointing the wrong direction, transformations applied in reverse order.

The addon ecosystem was hit hard. openFrameworks relies heavily on community-contributed "addons" (ofxAddons) for functionality like computer vision (ofxCv), physics (ofxBox2d), and GUI (ofxGui). Many addons expected ofVec3f parameters and could not accept glm::vec3 without modification. Since addons are maintained by individual developers — many of whom had moved on to other tools — hundreds of addons became incompatible with current oF versions.

## Notes

openFrameworks projects are particularly vulnerable to this kind of breakage because they are compiled C++ applications, not interpreted scripts. A Processing sketch from 2008 might still run in current Processing with minimal changes, but an oF project from 2014 requires the correct oF version, the correct compiler version, the correct OS SDK, and compatible versions of every addon — a dependency matrix that grows exponentially more fragile over time. Installation artworks built with oF are often locked to the specific laptop or desktop they were developed on.
