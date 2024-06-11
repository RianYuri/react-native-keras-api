import React from "react";
import {
  Active,
  Container,
  Divider,
  DropdownContent,
  Menu,
  MenuList,
  Select,
  SelectContainer,
  Selected,
  SelectedText,
  SelectionCat,
  TextSelects,
} from "./style";
import * as DocumentPicker from 'expo-document-picker';
import { router } from "expo-router";
import axios from "axios";
import { Button } from "react-native";
const Index = () => {
  const [isOpen, setIsOpen] = React.useState<boolean>(false);
  const handleListAnimal = () => {
    setIsOpen(!isOpen);
  };
  const [csvFile, setCsvFile] = React.useState<any>();
  const [selectedAnimal, setSelectedAnimal] = React.useState('Algoritmo Genético');

  const handleSelectActive = (value:string) =>{
    setSelectedAnimal(value)
  }
  const selectFile = async () => {
    let result = await DocumentPicker.getDocumentAsync({
      type: ["text/csv", "text/data"],
      multiple: false,
    });
 
    if (!result.canceled) {
      setCsvFile(result.assets[0]);
    }
  };
 
  const sendDataToAPI = async () => {
    const formData = new FormData();
    formData.append("algorithm", selectedAnimal);
 
    if (csvFile) {
      formData.append("database", {
        uri: csvFile.uri,
name: csvFile.name,
        type: "text/csv",
      } as any);
    }
 
    try {
const response = await axios.post("http://192.168.0.124:5000", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
 
      router.push({
        pathname: "/result",
        params: {
          data: JSON.stringify(response.data),
          algo: selectedAnimal,
        },
      });
    } catch (error) {
      console.error(error);
    }
  };
  return (
    <Container>
      <SelectContainer>
        <TextSelects>Selecione o algoritmo a ser usado</TextSelects>
        <DropdownContent>
          <Select onTouchStart={handleListAnimal}>
            <Selected>
              <SelectedText>{selectedAnimal}</SelectedText>
            </Selected>
          </Select>
          <Menu
            scrollEnabled
            isOpen={isOpen}
            style={{
              shadowColor: "#000",
              shadowOffset: { width: 0, height: 2 },
              shadowOpacity: 0.25,
              shadowRadius: 3.84,
              elevation: 3,
            }}
          >
            <MenuList>
              <React.Fragment>
                <SelectionCat onPress={()=>handleSelectActive('Algoritmo Genético')}>
                  <Active>Algoritmo Genetico</Active>
                </SelectionCat>
                  <Divider/>
                  <SelectionCat  onPress={()=>handleSelectActive('KNN')}>
                  <Active>Knn</Active>
                </SelectionCat>
                <Divider/>
                <SelectionCat  onPress={()=>handleSelectActive('Árvore de decisão')}>
                  <Active>Árvore de decisão</Active>
                </SelectionCat>
              </React.Fragment>
            </MenuList>
          </Menu>
        </DropdownContent>
        <Button title="Selecione o arquivo CSV" onPress={selectFile} />
 
  
         <Button title="Enviar" onPress={sendDataToAPI} />
      </SelectContainer>
    </Container>
  );
};

export default Index;
