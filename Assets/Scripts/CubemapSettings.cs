using System.Collections;
using System.Collections.Generic;
using UnityEngine;


[ExecuteInEditMode]
public class CubemapSettings : MonoBehaviour
{
    public float near;
    public float far;
    public float groundY;
    public Vector3 cubemapLoc;
    public bool showPartition;
    public Mode mode = Mode.Plane;
    private Material material;

    private Vector3 lastPosition;


    void OnEnable()
    {
        // sharedMaterial 
        material = GetComponent<Renderer>().sharedMaterial;
        UpdateMaterialProperties();
    }

    // triggered if variables on the inspector were changed
    void OnValidate()
    {
        UpdateMaterialProperties();
    }


    void Update()
    {
        if (transform.position != lastPosition)
        {
            lastPosition = transform.position;
            UpdateMaterialProperties();
        }
    }
    public void UpdateMaterialProperties()
    {
        if (material != null)
        {

            material.SetFloat("near", near);
            material.SetFloat("far", far);
            if (mode == Mode.Cube)
            {
                material.SetFloat("groundY", groundY);
                material.SetVector("cubemapLoc", transform.position);
            }
            else if (mode == Mode.Plane)
            {
                material.SetFloat("groundY", transform.position.y);
                material.SetVector("cubemapLoc", cubemapLoc);
            }



            
            material.SetInt("showPartition", showPartition ? 1 : 0);

            Debug.Log("updating shader variables");
        }
    }



}

public enum Mode
{
    Plane,
    Cube
}
