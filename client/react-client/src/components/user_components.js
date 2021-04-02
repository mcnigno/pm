import React, {useState, useEffect} from "react";
import axios from 'axios'


function Avatar (props) {
    const url = '/timesheetview/api/read'
    const [timesheet, setTimesheet] = useState(null)

    useEffect(() => {
        axios.get(url)
            .then(response => {
                setTimesheet(response.data.modelview_name)
                //console.log(response.data)
        })
    },[url])
   
    return  (
      <h1>Avatar {timesheet} {props.name}</h1>
    )
}

export default Avatar;

