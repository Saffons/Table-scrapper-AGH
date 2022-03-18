import { saveAs } from "file-saver";

const List = (props) => {

    const saveFile = (name) => {
        saveAs("../../db/" + name);
    }

    const scraps = props.scraps;
    return ( 
        <div className="scrap-list">
            {scraps.map((scrap) => (
                <div className="scraps-preview" key={scrap.id}>
                    <h2 onClick={() => saveFile(scrap.name)}>{scrap.name}</h2>
                    <p>Uploaded by {scrap.author}</p>
                    <a href={"../../db/" + scrap.csv} download>Download csv</a>
                </div>
            ))}
        </div>
     );
}
 
export default List;