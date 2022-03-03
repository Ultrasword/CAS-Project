package com.engine.handler;

public class Object {

    private static int idCount = 0;

    private int id;

    public Object(){
        this.id = genID();
    }

    private static int genID(){
        return idCount++;
    }

    public int getID(){
        return id;
    }

}
