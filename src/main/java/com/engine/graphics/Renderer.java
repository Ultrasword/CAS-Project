package com.engine.graphics;

import com.engine.graphics.VBOs.VertexBuffer;
import com.engine.handler.GameObject;

import java.util.concurrent.ConcurrentHashMap;

public class Renderer {
    /* TODO - Perfect and find any bugs
     */

    private ConcurrentHashMap<Integer, VertexBuffer> vboArray; // concurrent to allow multithreaded handling
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

    public <T extends VertexBuffer> void addVBO(T array){
        vboCount++;
        array.create();
        this.vboArray.put(vboCount, array);
        array.setRendererID(vboCount);
        System.out.println("GRAPHICS (Renderer.java): Added Array at position " + vboCount);
    }

    public void removeVBO(int id){
        this.vboArray.remove(id);
    }

    public <T extends GameObject> void addGameObject(T gameObject){
        int result = 0;
        for(int i = 1; i <= this.vboCount; i++){
            result = vboArray.get(i).addGameObject(gameObject);
            if (result!=0) {
                gameObject.setInVBO(true);
                gameObject.setVBOindex(i);
                System.out.println("GRAPHICS (Renderer.java): Added Entity");
                break;
            }
        }
        if (result == 0) System.out.println("VBO out of space!");
    }

    public void removeGameObject(int itemSlot, int vboID){
        this.vboArray.get(vboID).removeGameObject(itemSlot);
    }

    public void clean(){
        for(VBOobject vbo : vboArray.values()){
            vbo.clean();
        }
    }

    public int getVboCount() {
        return vboCount;
    }

    public ConcurrentHashMap<Integer, VertexBuffer> getVboArray() {
        return vboArray;
    }
}
