package com.engine.comp;

import org.joml.Vector4f;

public class ColourBi extends ColourMono {

    private Vector4f colour2;

    public ColourBi(){
        super();
    }

    public ColourBi(Vector4f c1, Vector4f c2){
        super();
        this.setColour(c1);
        colour2 = c2;
    }

    public Vector4f getColour2() {
        return colour2;
    }

    public void setColour2(Vector4f colour2) {
        this.colour2 = colour2;
    }


}
