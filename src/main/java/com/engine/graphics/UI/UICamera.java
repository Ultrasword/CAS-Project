package com.engine.graphics.UI;

import com.engine.graphics.Camera;
import com.engine.graphics.VBOs.UIVBO;
import org.joml.Vector3f;

public class UICamera extends Camera {

    private UIVBO uivbo;

    public UICamera(float width, float height, Vector3f position, float PIXSIZE, float near, float far) {
        super(width, height, position, PIXSIZE, near, far, 60f);
        adjustOrthoProjection();
        this.uivbo = new UIVBO(null, this);
        this.uivbo.create();
    }

    public void addUIObject(UIObject object){
        uivbo.addUIObject(object);
    }

    public void removeUIObject(int itemSlot){
        uivbo.removeUIObject(itemSlot);
    }

    public UIVBO getUivbo(){
        return uivbo;
    }



}
