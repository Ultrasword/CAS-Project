package com.engine.graphics;

import com.engine.handler.GameObject;

public abstract class VBOobject {
    protected int rendererID = 0; // 0 means it is not in a renderer

    public abstract void create();
    protected abstract void update();
    public abstract void bindShader();
    public abstract void unbindShader();
    public abstract void bindTextures();
    public abstract void unbindTextures();
    public abstract void render();
    public abstract void howToRender();
    public abstract void clean();
    public abstract <T extends GameObject> int addGameObject(T gameObject);
    public abstract void removeGameObject(int itemSlot);

    public int getRendererID() {
        return rendererID;
    }

    public void setRendererID(int rendererID) {
        this.rendererID = rendererID;
    }
}
