package com.engine.graphics;

import com.engine.utils.FileHandler;
import org.joml.*;
import org.lwjgl.BufferUtils;

import java.nio.FloatBuffer;

import static org.lwjgl.opengl.GL20.*;

public class Shader {
    private static int NULLSHADER = 0;

    private String vertexFile, fragFile;
    private String vertexShader, fragShader;
    private int vertexID, fragmentID, programID;

    public Shader(String vertex, String frag){
        this.vertexFile = vertex;
        this.fragFile = frag;
        this.vertexShader = FileHandler.loadAsString(vertexFile);
        this.fragShader = FileHandler.loadAsString(fragFile);
    }

    public void create(){
        // load the shaders
        vertexID = glCreateShader(GL_VERTEX_SHADER);
        // pass shader source to GPU
        glShaderSource(vertexID, vertexShader);
        glCompileShader(vertexID);

        // check for errors
        int success = glGetShaderi(vertexID, GL_COMPILE_STATUS);
        if (success == GL_FALSE){
            int len = glGetShaderi(vertexID, GL_INFO_LOG_LENGTH);
            System.err.println("ERROR: `" + vertexFile + "`.\nVertex shader compilation failed.");
            System.err.println(glGetShaderInfoLog(vertexID, len));
            assert false : "Error!";
        }

        // load the shaders
        fragmentID = glCreateShader(GL_FRAGMENT_SHADER);
        // pass shader source to GPU
        glShaderSource(fragmentID, fragShader);
        glCompileShader(fragmentID);

        // check for errors
        success = glGetShaderi(fragmentID, GL_COMPILE_STATUS);
        if (success == GL_FALSE){
            int len = glGetShaderi(fragmentID, GL_INFO_LOG_LENGTH);
            System.err.println("ERROR: `" + fragFile + "`.\nVertex shader compilation failed.");
            System.err.println(glGetShaderInfoLog(fragmentID, len));
            assert false : "Error!";
        }

        // link shaders
        programID = glCreateProgram();
        glAttachShader(programID, vertexID);
        glAttachShader(programID, fragmentID);
        glLinkProgram(programID);

        // look for linking progress
        success = glGetProgrami(programID, GL_LINK_STATUS);
        if (success == GL_FALSE){
            int len = glGetProgrami(programID, GL_INFO_LOG_LENGTH);
            System.err.println("ERROR: Shader Program could not be linked!");
            System.err.println(glGetProgramInfoLog(programID, len));
            assert false : "Error";
        }

    }

    public void bind(){
        glUseProgram(programID);
    }

    public void unbind(){
        glUseProgram(Shader.NULLSHADER);
    }

    public void clean(){
        glDeleteProgram(programID);
        glDeleteShader(vertexID);
        glDeleteShader(fragmentID);
    }

    public void uploadMat4f(String varName, Matrix4f mat4) {
        int varLocation = glGetUniformLocation(programID, varName);
        bind();
        FloatBuffer matBuffer = BufferUtils.createFloatBuffer(16);
        mat4.get(matBuffer);
        glUniformMatrix4fv(varLocation, false, matBuffer);
    }

    public void uploadMat3f(String varName, Matrix3f mat3) {
        int varLocation = glGetUniformLocation(programID, varName);
        bind();
        FloatBuffer matBuffer = BufferUtils.createFloatBuffer(9);
        mat3.get(matBuffer);
        glUniformMatrix3fv(varLocation, false, matBuffer);
    }

    public void uploadVec4f(String varName, Vector4f vec) {
        int varLocation = glGetUniformLocation(programID, varName);
        bind();
        glUniform4f(varLocation, vec.x, vec.y, vec.z, vec.w);
    }

    public void uploadVec3f(String varName, Vector3f vec) {
        int varLocation = glGetUniformLocation(programID, varName);
        bind();
        glUniform3f(varLocation, vec.x, vec.y, vec.z);
    }

    public void uploadVec2f(String varName, Vector2f vec) {
        int varLocation = glGetUniformLocation(programID, varName);
        bind();
        glUniform2f(varLocation, vec.x, vec.y);
    }

    public void uploadFloat(String varName, float val) {
        int varLocation = glGetUniformLocation(programID, varName);
        bind();
        glUniform1f(varLocation, val);
    }

    public void uploadInt(String varName, int val) {
        int varLocation = glGetUniformLocation(programID, varName);
        bind();
        glUniform1i(varLocation, val);
    }

    public void uploadTexture(String varName, int slot){
        int varLocation = glGetUniformLocation(programID, varName);
        bind();
        glUniform1i(varLocation, slot);
    }

    public void uploadIntArray(String varName, int[] data){
        int varLocation = glGetUniformLocation(programID, varName);
        bind();
        glUniform1iv(varLocation, data);
    }

    public String getVertexShader(){
        return vertexFile;
    }

    public String getFragShader(){
        return fragFile;
    }

}
