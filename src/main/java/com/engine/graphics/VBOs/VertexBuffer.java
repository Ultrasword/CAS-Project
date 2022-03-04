package com.engine.graphics.VBOs;

import com.engine.graphics.Shader;
import com.engine.graphics.Texture;
import com.engine.graphics.VBOobject;
import com.engine.handler.GameObject;
import com.engine.handler.SceneHandler;
import com.engine.utils.FileHandler;
import com.engine.utils.Time;

import java.util.ArrayList;
import java.util.List;

import static org.lwjgl.opengl.GL30.*;

public abstract class VertexBuffer extends VBOobject {

    public final static int FLOAT_BYTES = Float.BYTES;
    public final static int VERTICES_PER_ITEM = 4;
    public final static int MAX_ITEM_COUNT = 128;
    public final static int MAX_VERTEX_COUNT = MAX_ITEM_COUNT * VERTICES_PER_ITEM;
    public final static int VERTEX_SIZE = 3;
    public final static int COLOR_SIZE = 4;
    public final static int TEX_COORDS = 2;
    public final static int TEX_ID = 1;

    public final static int TEXTURE_BUFFER_SIZE = 9;

    public final static int INDICES_SIZE = MAX_VERTEX_COUNT * 3;
    public final static int INDICES_BUFFER_SIZE = INDICES_SIZE * FLOAT_BYTES;

    protected final int VERTEX_OBJECT_SIZE, VERTEX_OBJECT_SIZE_BYTES;
    protected final int vertexOffset, colorOffset, texOffset;
    protected final int ARRAY_BUFFER_SIZE, ARRAY_SIZE;

    protected Shader shader;
    protected String shaderPath = "/shaders/default";
    protected float[] array;
    protected int[] indices;
    protected int[] textures;
    protected boolean vertexArray, colorArray, texArray;
    protected boolean dirty, indicesWhereMade;
    protected int itemCount, attribCount, texCount;
    protected List<Texture> texSources;
    protected List<GameObject> dirtySprites;

    protected int vaoID, eboID, vboID;
    protected String validObject;

    public VertexBuffer(boolean vertexArray, boolean colorArray, boolean texArray, String shaderPath){
        this.vertexArray = vertexArray;
        this.colorArray = colorArray;
        this.texArray = texArray;
        VERTEX_OBJECT_SIZE = (vertexArray ? VERTEX_SIZE : 0) + (colorArray ? COLOR_SIZE : 0) + (texArray ? TEX_COORDS + TEX_ID : 0);
        attribCount = (vertexArray ? 1 : 0) + (colorArray ? 1 : 0) + (texArray ? 2 : 0);
        VERTEX_OBJECT_SIZE_BYTES = VERTEX_OBJECT_SIZE * FLOAT_BYTES;
        vertexOffset = 0;
        colorOffset = vertexOffset + (vertexArray ? VERTEX_SIZE : 0);
        texOffset = colorOffset + (colorArray ? COLOR_SIZE : 0);
        ARRAY_SIZE = VERTEX_OBJECT_SIZE * MAX_VERTEX_COUNT;
        ARRAY_BUFFER_SIZE = ARRAY_SIZE * FLOAT_BYTES;
        // stuff
        dirty=true;
        indicesWhereMade=false;
        if(shaderPath != null) this.shaderPath = shaderPath;
        this.dirtySprites = new ArrayList<>();

//        System.out.println(vertexOffset + " " + colorOffset + " " + texOffset + " " + VERTEX_OBJECT_SIZE);
//        System.out.println(ARRAY_SIZE + " " + ARRAY_BUFFER_SIZE);
    }

    public void create(){
        // this means that array sizes can be changed!
        // create arrays
        array = new float[ARRAY_SIZE];
        indices = new int[INDICES_SIZE];

        // System.out.println(shaderPath);
        // create shader
        shader = FileHandler.getShader(shaderPath);
        // create vertex array buffer
        vaoID = glGenVertexArrays();
        glBindVertexArray(vaoID);

        // Create VBO upload the vertex buffer
        vboID = glGenBuffers();
        glBindBuffer(GL_ARRAY_BUFFER, vboID);
        glBufferData(GL_ARRAY_BUFFER, array.length * FLOAT_BYTES, GL_DYNAMIC_DRAW);

        genIndices();
        eboID = glGenBuffers();
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, eboID);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW);

        // add vertex attribute pointers
        int position = 0, counter=0;
        if(vertexArray){
            glVertexAttribPointer(counter, VERTEX_SIZE, GL_FLOAT, false, VERTEX_OBJECT_SIZE_BYTES,
                    position * FLOAT_BYTES);
            position += VERTEX_SIZE;
            counter++;
        } if(colorArray){
            glVertexAttribPointer(counter, COLOR_SIZE, GL_FLOAT, false, VERTEX_OBJECT_SIZE_BYTES,
                    position * FLOAT_BYTES);
            position += COLOR_SIZE;
            counter++;
        } if(texArray){
            glVertexAttribPointer(counter, TEX_COORDS, GL_FLOAT, false, VERTEX_OBJECT_SIZE_BYTES,
                    position * FLOAT_BYTES);
            glVertexAttribPointer(counter+1, TEX_ID, GL_FLOAT, false, VERTEX_OBJECT_SIZE_BYTES,
                    (position+TEX_COORDS)*FLOAT_BYTES);
            position += TEX_COORDS + TEX_ID;
            counter+=2;
            // System.out.println(counter + " " + position);
            // create texture array
            textures = new int[]{0, 1, 2, 3, 4, 5, 6, 7, 8};
            texSources = new ArrayList<>();
        }
        // other stuff
    }

    public void update(){
        if (!indicesWhereMade){
            System.err.println("ERROR (VertexBuffer.java): You didnt CREATE UR INDICES in one of YOUR VBOs!");
            assert false : "Please make your indices u stupid man; smh";
        }
        this.cleanDirtySprites();
        if (this.dirty) {
            // System.out.println("GRAPHICS (VertexBuffer.java): Is dirty");
            glBindBuffer(GL_ARRAY_BUFFER, vboID);
            glBufferSubData(GL_ARRAY_BUFFER, 0, array);
            this.dirty = false;
        }
    }

    public void bindShader(){
        // make sure to find a way to detect changes
        shader.bind();
    }

    public void unbindShader(){
        shader.unbind();
    }

    public void bindTextures(){
        for(int i = 0; i < texSources.size(); i++) {
            glActiveTexture(GL_TEXTURE0 + i + 1);
            texSources.get(i).bind();
        }
        shader.uploadIntArray("tex", textures);
    }

    public void unbindTextures(){
        for(int i = 0; i < texSources.size(); i++)
            texSources.get(i).unbind();
    }

    public void render(){
        // enable vao
        glBindVertexArray(vaoID);
        // enable attrib pointers
        for(int i = 0; i < attribCount; i++)
            glEnableVertexAttribArray(i);
        // draw elements
        glDrawElements(GL_TRIANGLES, indices.length, GL_UNSIGNED_INT, 0);
        // disable attrib pointers
        for(int i = 0; i < attribCount; i++)
            glDisableVertexAttribArray(i);
        // unbind the vertex array
        glBindVertexArray(0);
        // TODO - decide whether or not to unbind the vertex array and the shader
    }

    public void removeGameObject(int itemSlot){
        int left = itemSlot * VERTEX_OBJECT_SIZE;
        int right = left + VERTEX_OBJECT_SIZE * 4;
        System.out.println("Removed at " + itemSlot);
        // get texID - use this data to change the thing if necassary
        int texID = (int)array[left+VERTEX_OBJECT_SIZE-1];
        for(int i = 0; i < right; i++){
            array[i] = 0;
        }
        this.dirty = true;
    }

    public abstract <T extends GameObject> void calculateVertices(T gameObject);

    public void cleanDirtySprites(){
        // System.out.println(this.dirtySprites.size());
        for(GameObject object : this.dirtySprites){
            calculateVertices(object);
        }
        this.dirtySprites.clear();
    }

    public abstract void howToRender();

    protected void genIndices(){
        indicesWhereMade = true;
        int offset, aOffset;
        for(int i = 0; i < MAX_ITEM_COUNT; i++){
            // standard 6 indices because of 4 vertices per item // standard tho - may chagne
            aOffset = i * 6;
            offset = i * VERTICES_PER_ITEM;
            // 3, 2, 0      0, 2, 1
            // br, tr, bl, tl
            // triangle 1
            indices[aOffset] = offset+3;
            indices[aOffset+1] = offset+2;
            indices[aOffset+2] = offset;
            // triangle2
            indices[aOffset+3] = offset;
            indices[aOffset+4] = offset+2;
            indices[aOffset+5] = offset+1;
        }
    }

    public void clean(){
        this.dirtySprites.clear();
        this.unbindShader();
        this.unbindTextures();
        glDeleteVertexArrays(vaoID);
        glDeleteBuffers(vboID);
        glDeleteBuffers(eboID);
    }

    public String getShaderPath(){
        return this.shaderPath;
    }

    public void setShader(String path){
        this.shaderPath = path;
    }

    public boolean hasIndices(){
        return indicesWhereMade;
    }

    public boolean hasSpace(){
        return itemCount >= MAX_ITEM_COUNT;
    }

    public boolean isDirty(){
        return this.dirty;
    }

    public boolean hasTexSpace(){
        return this.texCount <= TEXTURE_BUFFER_SIZE;
    }

    public String getValidObject() {
        return validObject;
    }

    public void setValidObject(String validObject) {
        this.validObject = validObject;
    }

    public void addDirtySprite(GameObject gameObject){
        this.dirtySprites.add(gameObject);
    }
}
