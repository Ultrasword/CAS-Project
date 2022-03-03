package com.engine.utils;

import com.engine.graphics.Shader;
import com.engine.graphics.Texture;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;

public class FileHandler {

    public static HashMap<String, Shader> shaderMap = new HashMap<>();
    public static HashMap<String, Texture> textureMap = new HashMap<>();

    public static String loadAsString(String path){
        StringBuilder result = new StringBuilder();
        // System.out.println(path);
        try(BufferedReader reader = new BufferedReader(new InputStreamReader(FileHandler.class.getResourceAsStream(path)))){
            String line = "";
            while ((line=reader.readLine()) != null){
                result.append(line + "\n");
            }
        } catch(IOException e){
            System.err.println("The file located at `" + path + "` could not be found. Aborting operation.");
        } catch(Exception e){
            e.printStackTrace();
        }
        return result.toString();
    }

    public static Texture getTexture(String path){
        if (textureMap.containsKey(path)) return textureMap.get(path);
        Texture tex = new Texture(path);
        textureMap.put(path, tex);
        return tex;
    }

    public static Shader getShader(String shaderName) {
        if (shaderMap.containsKey(shaderName)) return shaderMap.get(shaderName);
        if (shaderName.endsWith(".glsl")) System.out.println("ERROR (FileHandler): You have inputted the full file path. " +
                "\nMake sure to only input the base file name with {folder}/{name}. Code will auto add .glsl and v and f!");
        Shader shader = new Shader(shaderName + "v.glsl", shaderName + "f.glsl");
        shader.create();
        shaderMap.put(shaderName, shader);
        return shader;
    }

    public static void close(){
        // clean shaders
        for (Shader shader : shaderMap.values()){
            shader.unbind();
            shader.clean();
            // log
            System.out.println("CLEAN (FileHandler.java): Cleaned out shader at `" + shader.getVertexShader()
                    + "` and `" +  shader.getFragShader() + "`!");
        }
        // clean textures
        for (Texture tex : textureMap.values()){
            tex.unbind();
            tex.clean();
            System.out.println("CLEAN (FileHandler.java): Cleaned out texture at `" + tex.getPath() + "`!");
        }
    }

}
