package com.engine.comp;

public abstract class Component {

    protected String name = "Base";

    public abstract void update(float dt);

    public String getName(){
        return name;
    }

}
