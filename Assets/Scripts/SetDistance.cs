using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class SetDistance : MonoBehaviour
{
    public string filename = "distances.csv";
    private List<float> distances = new List<float>();

    private Animator animator;
    private AnimationClip animationClip;
    private float animationDuration;
    private float frameRate;
    private int totalFrames;
    private int counter;

    void Start()
    {
        animator = GetComponent<Animator>();
        animationClip = animator.runtimeAnimatorController.animationClips[0];
        animationDuration = animationClip.length;
        frameRate = 1f;
        totalFrames = Mathf.RoundToInt(animationDuration * frameRate);

        LoadCSV();

    }

    void Update()
    {
        float currentTime = animator.GetCurrentAnimatorStateInfo(0).normalizedTime;
        currentTime = currentTime % 1f;

        int currentFrame = Mathf.FloorToInt(currentTime * animationDuration * frameRate);
        currentFrame = Mathf.Clamp(currentFrame, 0, distances.Count - 1);
        
        float distance = distances[currentFrame];

        Vector3 currentPosition = transform.position;
        transform.position = new Vector3(currentPosition.x, currentPosition.y, distance);

        counter++;
        Debug.Log(counter + ": " + distance);

    }

    void LoadCSV()
    {
        string filePath = Path.Combine(Application.dataPath, filename);
        StreamReader reader = new StreamReader(filePath);

        while (!reader.EndOfStream)
        {
            string line = reader.ReadLine();
            distances.Add(float.Parse(line) + 50);
        }

        reader.Close();
    }
}
