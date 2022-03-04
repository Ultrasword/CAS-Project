package com.engine.handler;

import com.engine.graphics.Camera;

public abstract class Scene {

    protected Camera camera;

    public abstract void update(float dt);
    public abstract void render();

    public Camera getCamera() {
        return camera;
    }

    public void setCamera(Camera camera) {
        this.camera = camera;
    }
}
