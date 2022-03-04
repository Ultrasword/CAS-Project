package com.engine.handler.Entities;

import com.engine.handler.GameObject;
import com.engine.handler.Transform2D;
import org.joml.Vector2f;
import org.joml.Vector3f;

public class GameEntity2D extends GameObject {

    public GameEntity2D(){
        super();
    }

    public GameEntity2D(Transform2D transform){
        this.transform = transform;
    }

    public void update(float dt) {
        updateComponents(dt);
    }

    public void setPosition(Vector3f position){
        transform.setPosition(position);
        setDirty();
    }

    public Vector3f getPosition(){
        return transform.getPosition();
    }

    public Vector2f getScale() {
        return transform.getScale();
    }

    public void setScale(Vector2f scale) {
         transform.setScale(scale);
         setDirty();
    }

    public float getRotation() {
        return transform.getRotation();
    }

    public void setRotation(float rotation) {
        transform.setRotation(rotation);
        setDirty();
    }

    public Transform2D getTransform(){
        return transform;
    }


}
