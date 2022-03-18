import React, { useState } from "react";
import useFetch from "./useFetch";
import { variables } from "./Variables";

class Scrap extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            id: 0,
            name: "",
            author: "",
            csv: "",
            path:variables.PHOTO_URL
        }
    }

    changeName = (e) => {
        var fullPath = document.getElementById('upload').value;
        if (fullPath) {
            var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
            var filename = fullPath.substring(startIndex);
            if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
                filename = filename.substring(1);
            }
            alert(filename);
        }
        this.setState({ name: filename });
        this.imageUpload(e);
        console.log(this.state.name);
    }
    
    changeAuthor = (e) => {
        this.setState({ author: e.target.value });
        console.log(this.state.author);
    }

    imageUpload = (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append('file', e.target.files[0], e.target.files[0].name);

        fetch(variables.API_URL+"scrap/save", {
            method:'POST',
            body:formData
        })
        .then(res=>res.json() 
            
        )
        .then(data=>{
            //this.setState({name:data}); 
        })
    }

    createClick() {
        console.log('ddddd');
        fetch(variables.API_URL + "api/scrap", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                author: this.state.author,
                name: this.state.name,
                csv: this.state.name + ".csv"
            })
        })
            .then(res => res.json())
            .then((result) => {
                alert(result);
            }, (error) => {
                alert('failed');
            })
    }

    render() {
        const {
            id,
            author,
            name,
            csv,
            path
        } = this.state;

        return (
            <div className="scrap">

                <h1>Scrap a table</h1>
                <button id="scrapButton" onClick={()=>this.createClick()}>Scrap</button>
                <br></br>
                <p>Author</p>
                <input name="author" id="author" onChange={this.changeAuthor} ></input>
                <br></br>
                <p>Upload</p>
                <input name="upload" id="upload" type="file" onChange={this.changeName} ></input>


            </div>

            

        );
    }
}
export default Scrap;