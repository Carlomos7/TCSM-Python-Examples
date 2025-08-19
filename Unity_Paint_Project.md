# Unity Paint System Tutorial

## Overview
This tutorial will guide you through creating a 3D paint system in Unity using C# scripts. The system allows users to create, destroy, and customize 3D objects by clicking and interacting with the scene.

## Table of Contents
1. [Project Setup](#project-setup)
2. [Core Concepts](#core-concepts)
3. [Implementation Steps](#implementation-steps)
4. [Script Breakdown](#script-breakdown)
5. [Advanced Features](#advanced-features)
6. [Best Practices](#best-practices)

## Project Setup

### Prerequisites
- Unity 2020.3 LTS or later
- Basic understanding of C# programming
- Familiarity with Unity's Transform and GameObject systems

### Initial Setup
1. Create a new Unity 3D project
2. Set up your main scene with a Camera and directional light
3. Create an empty GameObject to serve as the paint manager
4. Add UI elements for controls (Canvas, Buttons, Sliders, Text)

## Core Concepts

### 1. Screen to World Position Conversion
The foundation of the paint system is converting mouse screen coordinates to 3D world positions.

### 2. Raycasting
Used for detecting clicks on objects and determining precise world positions.

### 3. Object Instantiation
Creating primitive shapes or custom prefabs at calculated positions.

### 4. Color and Size Manipulation
Dynamically changing object properties based on user input.

## Implementation Steps

### Step 1: Basic Object Creation

Create a simple script that spawns objects on mouse click:

```csharp
using UnityEngine;

public class CreateSimpleObjects : MonoBehaviour
{
    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            // Create a cylinder at origin (basic implementation)
            GameObject cylinder = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        } 
    }
}
```

### Step 2: Screen to World Point Conversion

Improve the basic system by placing objects at mouse position:

```csharp
using UnityEngine;

public class ClickPositionManager_01ScreenToWorldPoint : MonoBehaviour
{
    public float distance = 3f;
    public GameObject fancy; // Optional prefab
    public float distanceChange = 1f;

    private void Update()
    {
        if (Input.GetMouseButtonDown(0) || Input.GetMouseButton(1))
        {
            distance += distanceChange;
            
            // Convert screen position to world position
            Vector3 clickPosition = Camera.main.ScreenToWorldPoint(
                Input.mousePosition + new Vector3(0f, 0f, distance)
            );
            
            Debug.Log(clickPosition);
            
            // Option 1: Create primitive
            // GameObject sphere = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            // sphere.transform.position = clickPosition;
            
            // Option 2: Instantiate prefab
            if (fancy != null)
                Instantiate(fancy, clickPosition, Quaternion.identity);
        }
    }
}
```

### Step 3: Raycast-Based Positioning

Use raycasting for more accurate positioning on surfaces:

```csharp
using UnityEngine;

public class ClickPositionManager_02ScreenPointToRay : MonoBehaviour
{
    public LayerMask clickMask; // Specify which layers to hit

    void Update()
    {
        if (Input.GetMouseButtonDown(0) || Input.GetMouseButton(1))
        {
            Vector3 clickPosition = -Vector3.one;
            
            // Cast ray from camera through mouse position
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit hit;
            
            if (Physics.Raycast(ray, out hit, 100f, clickMask))
            {
                clickPosition = hit.point;
                GameObject primitive = GameObject.CreatePrimitive(PrimitiveType.Sphere);
                primitive.transform.position = clickPosition;
            }
            
            Debug.Log(clickPosition);
        }
    }
}
```

### Step 4: Plane-Based Raycast

For consistent placement on a virtual plane:

```csharp
using UnityEngine;

public class ClickPositionManger_03PlaneRaycast : MonoBehaviour
{
    private GameObject primitive;

    void Update()
    {
        if (Input.GetMouseButtonDown(0) || Input.GetMouseButton(1))
        {
            Vector3 clickPosition = -Vector3.one;
            
            // Create an invisible plane for consistent positioning
            Plane plane = new Plane(Vector3.forward, 0f); // or Vector3.up for horizontal plane
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            float distanceToPlane;
            
            if (plane.Raycast(ray, out distanceToPlane))
            {
                clickPosition = ray.GetPoint(distanceToPlane);
            }
            
            Debug.Log(clickPosition);
            primitive = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            primitive.transform.position = clickPosition;
        }   
    }
}
```

## Script Breakdown

### Main Paint Manager: ClickPositionManager_Sprint03

This is the complete paint system with all features:

```csharp
using UnityEngine;
using UnityEngine.UI;

public class ClickPositionManager_Sprint03 : MonoBehaviour
{
    // Shape selection (0=Sphere, 1=Cylinder, 2=Cube, 3=Capsule)
    private int shape = 0;
    private GameObject primitive;
    
    // Color controls (RGB values)
    private float red = 1f, green = 1f, blue = 1f;
    
    // UI reference
    public Text mousePosition;
    
    // Distance and size controls
    [SerializeField]
    private float distance = 5f, distranceChange;
    private Vector3 clickPosition;
    private bool timedDestroyIsOn = true;
    private float size = 0.5f;

    void Update()
    {
        // Left mouse button: Destroy objects
        if (Input.GetMouseButtonDown(0) || Input.GetMouseButton(0))
        {
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit hit;

            if (Physics.Raycast(ray, out hit))
            {
                Destroy(hit.transform.gameObject);
            }
        }
        
        // Right mouse button: Create objects
        if (Input.GetMouseButtonDown(1) || Input.GetMouseButton(1))
        {
            // Calculate world position
            clickPosition = Camera.main.ScreenToWorldPoint(
                Input.mousePosition + new Vector3(0f, 0f, distance)
            );

            // Create shape based on current selection
            switch (shape)
            {
                case 0: primitive = GameObject.CreatePrimitive(PrimitiveType.Sphere); break;
                case 1: primitive = GameObject.CreatePrimitive(PrimitiveType.Cylinder); break;
                case 2: primitive = GameObject.CreatePrimitive(PrimitiveType.Cube); break;
                case 3: primitive = GameObject.CreatePrimitive(PrimitiveType.Capsule); break;
            }
            
            // Apply random scale within size limits
            primitive.transform.localScale = new Vector3(
                Random.Range(0.1f, 1f) * size,
                Random.Range(0.1f, 1f) * size,
                Random.Range(0.1f, 1f) * size
            );
            
            // Set position and random color
            primitive.transform.position = clickPosition;
            primitive.GetComponent<Renderer>().material.color = new Vector4(
                Random.Range(0f, red),
                Random.Range(0f, green),
                Random.Range(0f, blue),
                1f
            );
            
            // Optional timed destruction
            if (timedDestroyIsOn)
            {
                Destroy(primitive, 3f);
            }
        }
        
        // Update UI with mouse position
        mousePosition.text = "Mouse Position \nX: " + Input.mousePosition.x.ToString("F0") + 
                           "\nY: " + Input.mousePosition.y.ToString("F0");
    }
    
    // Public methods for UI controls
    public void changeShape(int tempShape) { shape = tempShape; }
    public void changeRed(float tempRed) { red = tempRed; }
    public void changeGreen(float tempGreen) { green = tempGreen; }
    public void changeBlue(float tempBlue) { blue = tempBlue; }
    public void ChangeSize(float tempSize) { size = tempSize; }
    public void ToggleTimedDestroy(bool timer) { timedDestroyIsOn = timer; }
    
    public void destroyObjects()
    {
        // Destroy all child objects
        foreach (Transform child in transform)
        {
            Destroy(child.gameObject);
        }
    }
}
```

## Advanced Features

### 1. Shape Selection System
- Use integer values to represent different primitive types
- Switch statements for clean shape creation logic
- UI buttons connected to `changeShape()` method

### 2. Color Control System
- RGB sliders connected to color change methods
- Random color generation within specified ranges
- Real-time color preview

### 3. Size and Scale Control
- Global size multiplier
- Random scale variation for organic feel
- UI slider for size adjustment

### 4. Object Destruction
- Left-click raycast destruction
- Timed auto-destruction option
- Clear all objects functionality

### 5. UI Integration
- Mouse position display
- Real-time feedback
- Control panels for all features

## Best Practices

### Performance Optimization
1. **Object Pooling**: For better performance with many objects
2. **Layer Masks**: Use specific layers for raycast targets
3. **LOD Systems**: Implement level-of-detail for complex scenes

### Code Organization
1. **Separation of Concerns**: Split UI logic from painting logic
2. **Event Systems**: Use Unity Events for UI communication
3. **Configuration**: Use ScriptableObjects for paint settings

### User Experience
1. **Visual Feedback**: Cursor changes, preview objects
2. **Undo System**: Track and reverse actions
3. **Save/Load**: Persist painted scenes

### Error Handling
```csharp
// Always check for null references
if (Camera.main != null)
{
    Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
    // ... raycast logic
}

// Validate UI components
if (mousePosition != null)
{
    mousePosition.text = "Mouse Position: " + Input.mousePosition;
}
```

## Extensions and Improvements

### 1. Brush System
- Different brush types and sizes
- Texture painting on surfaces
- Particle effects for paint trails

### 2. Advanced Materials
- Custom shaders for paint effects
- Metallic and roughness controls
- Texture mapping

### 3. 3D Sculpting
- Vertex manipulation
- Mesh deformation
- Sculpting tools (push, pull, smooth)

### 4. Collaboration Features
- Multi-user painting
- Real-time synchronization
- Version control for artwork

## Conclusion

This paint system provides a solid foundation for 3D creative applications in Unity. The modular approach allows for easy extension and customization. Start with the basic implementation and gradually add features based on your project requirements.

Remember to test thoroughly, optimize for your target platform, and always consider the user experience when adding new features.

## Troubleshooting

### Common Issues:
1. **Objects not appearing**: Check camera distance and positioning
2. **Raycast not working**: Verify layer masks and colliders
3. **UI not updating**: Ensure proper component references
4. **Performance issues**: Implement object pooling and cleanup systems

### Debug Tips:
- Use `Debug.Log()` to track position calculations
- Enable Gizmos to visualize raycasts
- Use Unity's Frame Debugger for rendering issues
- Profile with Unity Profiler for performance bottlenecks
