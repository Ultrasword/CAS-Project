package com.engine;

import org.joml.Matrix4f;
import org.joml.Vector3f;

public class Camera {

    private float PIXELSIZE;
    private float width, height;
    private float near, far, fov;

    private Vector3f eye, rotation, translation, up;
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
        this.up = new Vector3f(0, 1f, 0);
    }

    public void adjustOrthoProjection(){
        projMatrix.identity(); //  returns a special matrix - 1
        projMatrix.ortho(0.0f, PIXELSIZE * width, 0.0f, PIXELSIZE * height, near, far);
    }

    public void adjustFrustrumProjection(){
        float aspect = width / height;
        float left = -width / 2f;
        float right = width / 2f;
        float bottom = -height / 2f;
        float top = height / 2f;
        float near = 0.0001f;
        float far = 10000.0f;

        projMatrix.identity();
        projMatrix.perspective(fov, aspect, near, far);
    }

    public Matrix4f getViewMatrix(){
        viewMatrix.identity();
        viewMatrix.lookAt(new Vector3f(eye.x, eye.y, 0.0f), this.eye, up);
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

    public void setPosition(Vector3f pos){
        this.translation.x = pos.x;
        this.translation.y = pos.y;
        this.translation.z = pos.z;
    }

    public void setPosition(float x, float y, float z){
        this.translation.x = x;
        this.translation.y = y;
        this.translation.z = z;
    }

    //TODO - rotation and stuff - fix this garbage
    public void rotate(Vector3f rotation){
        this.rotation.add(rotation);
    }

    public void rotate(float x, float y, float z){
        this.rotation.add(x, y, z);
    }

    public void setRotation(Vector3f rotation){
        this.rotation.x = rotation.x;
        this.rotation.y = rotation.y;
        this.rotation.z = rotation.z;
    }

    public void setRotation(float x, float y, float z){
        this.rotation.x = x;
        this.rotation.y = y;
        this.rotation.z = z;
    }


}
