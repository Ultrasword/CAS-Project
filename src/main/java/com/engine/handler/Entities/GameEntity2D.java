package com.engine.handler.Entities;

import com.engine.event.DirtyEvent;
import com.engine.event.EventQueue;
import com.engine.handler.GameObject;
import com.engine.handler.Transform2D;
import org.joml.Vector2f;
import org.joml.Vector3f;

public class GameEntity2D extends GameObject {

    protected Transform2D transform;

    public GameEntity2D(){
        super();
    }

    public GameEntity2D(Transform2D transform){
        this.transform = transform;
    }

    protected void update(float dt) {
        setRotation(getRotation()+20*dt);
    }

    public void setPosition(Vector3f position){
        transform.setPosition(position);
        Dirty();
    }

    public Vector3f getPosition(){
        return transform.getPosition();
    }

    public Vector2f getScale() {
        return transform.getScale();
    }

    public void setScale(Vector2f scale) {
         transform.setScale(scale);
         Dirty();
    }

    public float getRotation() {
        return transform.getRotation();
    }

    public void setRotation(float rotation) {
        transform.setRotation(rotation);
        Dirty();
    }

    public Transform2D getTransform(){
        return transform;
    }


}
