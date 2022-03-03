package com.engine;

import org.joml.Matrix4f;
import org.joml.Vector3f;

public class Camera {

    private float PIXELSIZE;
    private float width, height;
    private float near, far, fov;

    private Vector3f eye, rotation, translation;
    private Matrix4f projMatrix, viewMatrix;

    public Camera(float width, float height, Vector3f position, float PIXSIZE, float near, float far, float fov){
        // sets initial position to 0, 0, 0
        this.width = width;
        this.height = height;
        this.fov = fov;
        this.projMatrix = new Matrix4f();
        this.viewMatrix = new Matrix4f();
        this.PIXELSIZE = PIXSIZE;
        this.near = near;
        this.far = far;
        // some view matrix variables
        this.eye = position;     // what camera is looking at
        this.rotation = new Vector3f(0.0f, 1.0f, 0.0f);         // rotation of camera
        this.translation = new Vector3f();
    }

    public void adjustOrthoProjection(){
        projMatrix.identity(); //  returns a special matrix - 1
        projMatrix.ortho(0.0f, PIXELSIZE * width, 0.0f, PIXELSIZE * height, near, far);
    }

    public void adjustFrustrumProjection(){
        projMatrix.identity();
        projMatrix.frustum(0f, 0f, width, height, near, far);
        projMatrix.lookAt(new Vector3f(eye.x, eye.y, 0.0f), eye, rotation);
    }

    public Matrix4f getViewMatrix(){
        viewMatrix.identity();
        viewMatrix.lookAt(new Vector3f(eye.x, eye.y, 0.0f),
                eye, rotation);
        return viewMatrix;
    }

    public Matrix4f getProjMatrix(){
        return projMatrix;
    }

    public Matrix4f getViewProjMatrix(){
        // find a way to get a copy of the object and not a reference
        Matrix4f copy = getProjMatrix();
        return getViewMatrix();
    }

    public void update(){
        this.eye.add(translation);
        translation.x = 0.0f; translation.y = 0.0f; translation.z = 0.0f;
    }

    public void setNewDimensions(int w, int h){
        this.width = (float)w;
        this.height = (float)h;
        // System.out.println(this.width + " " + this.height);
    }

    public void move(float x, float y, float z){
        this.translation.x += x;
        this.translation.y += y;
        this.translation.z += z;
    }

    public void move(Vector3f translate){
        this.translation.add(translate);
    }

}
