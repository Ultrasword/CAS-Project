package com.engine.graphics;

import java.util.concurrent.ConcurrentHashMap;

public class Renderer {
    /* TODO - FINISH THIS
        this class holds all the VBOobjects
        it also allows you to add different gameobjects to the array
        this renderer object can hold one subclass of vertexbufferobjects
        all of them can be rendered
        a hashmap will hold the items
     */

    private ConcurrentHashMap<Integer, VBOobject> vboArray; // concurrent to allow multithreaded handling
    private int vboCount = 0;

    public Renderer(){
        vboArray = new ConcurrentHashMap<>();

    }

    public void renderArrays(){
        for(VBOobject vbo : vboArray.values()){
            vbo.update();
            vbo.howToRender();
        }
    }

    public <T extends VBOobject> void addVBO(T array){
        vboCount++;
        this.vboArray.put(vboCount, array);
        array.setRendererID(vboCount);
    }

    public void removeVBO(int id){
        this.vboArray.remove(id);
    }

    public void clean(){
        for(VBOobject vbo : vboArray.values()){
            vbo.clean();
        }
    }

}
