package com.engine.handler;

import com.engine.Camera;
import com.engine.graphics.Renderer;

public abstract class Scene {

    protected Camera camera;
    protected EntityHandler entityHandler;
    protected Renderer renderer;

    public abstract void update(float dt);
    public abstract void render();

    public Camera getCamera() {
        return camera;
    }

    public void setCamera(Camera camera) {
        this.camera = camera;
    }

    public void start(){ }

    public <T extends GameObject> void addGameObject(T gameObject){
        this.entityHandler.addGameObject(gameObject);
        this.renderer.addGameObject(gameObject);
        gameObject.start();
    }

    public void removeGameObject(long uid, int itemSlot, int vboArray){
        this.entityHandler.removeGameobject(uid);
        this.renderer.removeGameObject(itemSlot, vboArray);
    }

    public void clean(){
        entityHandler.clean();
        renderer.clean();
    }

    public EntityHandler getEntityHandler() {
        return entityHandler;
    }

    public void setEntityHandler(EntityHandler entityHandler) {
        this.entityHandler = entityHandler;
    }

    public Renderer getRenderer() {
        return renderer;
    }

    public void setRenderer(Renderer renderer) {
        this.renderer = renderer;
    }
}
