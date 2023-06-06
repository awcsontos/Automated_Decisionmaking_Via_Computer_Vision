using System.Collections;
using System;
using System.Diagnostics;
using UnityEditor.Scripting.Python;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class Movement : MonoBehaviour
{
	public float speed = 1.0f;
	private Rigidbody rb;
	public Camera cam;
	public Vector3 movement = new Vector3(0, 0, -10);
	public string decision;
	private string gotDecision;
	private int frames = 0;
	private int counter = 0;
	private HelloRequester _helloRequester;
    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void FixedUpdate()
    {
		if (frames % 30 == 0) 
		{ 
        	decision = getDecision();
		}
		frames++;
		
		//Comment out either automated or user input for debugging.
        if(decision == "forward")
		//if(Input.GetKeyDown(KeyCode.W))
		{
			movement = new Vector3(0, 0, -10);
			forward();
		}
		else if(decision == "left")
		//if(Input.GetKeyDown(KeyCode.A))
		{
			if (frames % 30 == 0) 
			{ 
				left();
			}
			forward();
		}
		else if(decision == "right")
		//if(Input.GetKeyDown(KeyCode.D))
		{
			if (frames % 30 == 0) 
			{ 
				right();
			}
			forward();
		}
		else if(decision == "turnAround")
		//if(Input.GetKeyDown(KeyCode.S))
		{
			if (frames % 30 == 0) 
			{ 
				turnAround();
			}
			forward();
		}
		//if(Input.GetKeyDown(KeyCode.F9))
		//{
		//	SaveCameraView(cam);
		//}
    }
	
	void forward()
	{
		rb.AddForce(movement * speed);
	}
	
	void right()
	{
		movement = new Vector3(-10, 0, 0);
		transform.Rotate(0.0f, 90.0f, 0.0f);
	}
	
	void left()
	{
		movement = new Vector3(10, 0, 0);
		transform.Rotate(0.0f, -90.0f, 0.0f);
	}
	
	void turnAround()
	{
		movement = -1 * movement;
		transform.Rotate(0.0f, -180.0f, 0.0f);
	}
	
	string getDecision()
	{
		int numchoices = getChoices();
		string[] choices = {"forward", "left", "right", "turnAround"};
		return choices[numchoices];
		
	}
	
	void SaveCameraView(Camera cam)
	{
		RenderTexture screenTexture = new RenderTexture(Screen.width, Screen.height, 16);
		cam.targetTexture = screenTexture;
		RenderTexture.active = screenTexture;
		cam.Render();
		Texture2D renderedTexture = new Texture2D(Screen.width, Screen.height);
		renderedTexture.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
		RenderTexture.active = null;
		byte[] byteArray = renderedTexture.EncodeToPNG();
		System.IO.File.WriteAllBytes("Assets/decisionScreenshot" + "/cameracapture" + counter + ".png", byteArray);
		counter++;
		UnityEditor.AssetDatabase.Refresh();
	}

	
	int getChoices()
	{
		SaveCameraView(cam);
		_helloRequester = new HelloRequester();
        _helloRequester.Start();
		string choice = _helloRequester.Stop();
		if(choice == "turn_around" || choice == "dead_end")
		{
			return 3;
		}
		if(choice == "left" || choice == "left_or_right")
		{
			return 1;
		}
		if(choice == "right" || choice == "right_or_straight")
		{
			return 2;
		}
		if(choice == "straight" || choice == "right_or_straight")
		{
			return 0;
		}
		else
		{
			return -1;
		}
	}
}
