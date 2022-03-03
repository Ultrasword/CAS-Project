package com.engine.handler;

import org.joml.Vector2f;
import org.joml.Vector3f;

public class Transform2D {

    private Vector3f position;
    private Vector2f scale;
    private float rotation;

    public Transform2D(){
        position = new Vector3f();
        scale = new Vector2f(1);
        rotation = 0f;
    }

    public Transform2D(Vector3f position){
        this.position = position;
        this.rotation = 0f;
        this.scale = new Vector2f(1);
        this.position.z *= -1;
    }

    public Transform2D(Vector3f position, Vector2f scale){
        this.scale = scale;
        this.position = position;
        this.rotation = 0f;
        this.position.z *= -1;
    }

    public Transform2D(Vector3f position, Vector2f scale, float rotation){
        this.scale = scale;
        this.position = position;
        this.rotation = rotation;
        this.position.z *= -1;
    }

    public Transform2D copy(){
        return new Transform2D(this.position, this.scale, this.rotation);
    }

    public Vector3f getPosition() {
        return position;
    }

    public void setPosition(Vector3f position) {
        this.position = position;
    }

    public Vector2f getScale() {
        return scale;
    }

    public void setScale(Vector2f scale) {
        this.scale = scale;
    }

    public float getRotation() {
        return rotation;
    }

    public void setRotation(float rotation) {
        this.rotation = rotation;
    }

    public boolean equals(Transform2D other){
        if (!this.position.equals(other.position)) return false;
        if (!this.scale.equals(other.scale)) return false;
        if (this.rotation != other.rotation) return false;
        return true;
    }

    public String toString(){
        return String.format("Pos: %s, %s | Scale: %s, %s | Rot: %.2f", position.x, position.y, scale.x, scale.y, rotation);
    }
}
