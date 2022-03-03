package com.engine.comp;

import org.joml.Vector4f;

public class ColourMono extends Component{

    private Vector4f colour;

    public ColourMono(){
        super();
    }

    public ColourMono(Vector4f colour){
        super();
        this.colour = colour;
    }

    @Override
    public void update(float dt) {

    }

    public Vector4f getColour() {
        return colour;
    }

    public void setColour(Vector4f colour) {
        this.colour = colour;
    }

}
