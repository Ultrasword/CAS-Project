package com.engine.graphics.UI;

import com.engine.graphics.Texture;
import com.engine.handler.GameObject;
import com.engine.handler.Transform2D;
import com.engine.utils.FileHandler;

public class UIObject extends GameObject {

    public final static float[] texCoords = {1f, 0f, 1f, 1f, 0f, 1f, 0f, 0f};

    private int texID;
    private Transform2D transform2D;
    private boolean inVBO;
    private Texture texture;

    public UIObject(Transform2D transform2D, String texturePath){
        super();
        // create texture
        this.texture = FileHandler.getTexture(texturePath);
        this.texID = this.texture.getTexID();
        this.transform2D = transform2D;
        this.inVBO = false;
    }

    public UIObject(Transform2D transform2D, Texture texture){
        super();
        // do stuff with texture
        this.texture = texture;
        this.texID = texture.getTexID();
        this.transform2D = transform2D;
        this.inVBO = false;
    }

    public int getTexID() {
        return texID;
    }

    public void changeTexture(String path) {
        this.texID = FileHandler.getTexture(path).getTexID();
    }

    public Transform2D getTransform2D() {
        return transform2D;
    }

    public void setTransform2D(Transform2D transform2D) {
        this.transform2D = transform2D;
    }

    // if object already in a vbo
    public boolean isInVBO() {
        return inVBO;
    }

    public void setInVBO(boolean inVBO) {
        this.inVBO = inVBO;
    }

    public Texture getTexture() {
        return texture;
    }
}
