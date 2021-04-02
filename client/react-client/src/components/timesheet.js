import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
import BootstrapTable from 'react-bootstrap-table-next'
import React, {Component, useEffect,useState} from 'react';
import axios from 'axios';

function Timesheet (props) {
    
    const url = '/timesheetview/api/read'
    const [timesheet, setTimesheet] = useState(null)

    useEffect(() => {
        axios.get(url)
            .then((response) => {
                var labels = []
                response.data.list_columns.forEach((element,index) => {
                labels[index]= {title:response.data.label_columns[element], field:element}
                
                })
                labels.push({
                    field: 'action',
                    title: 'Actions',
                    align: 'center',
                    formatter: function () {
                    return '<a href="javascript:" class="like"><i class="fa fa-star"></i></a>'
                    },
                    events: {
                    'click .like': function (e, value, row) {
                        alert(JSON.stringify(row))
                    }
                    }
                })
                response.data['labels'] = labels
                
                setTimesheet(response.data)
                console.log('timesheet result')
                console.log(timesheet)
        })
    },[])
    if (timesheet){
        return  (
            //<p>timesheet</p>
            //<p>{timesheet.modelview_name}</p>
            <BootstrapTable keyField='id' data={ timesheet.result } columns={ timesheet.labels } />
        )

    }
    return  (
        <p>Loading ...</p>
        //<p>{timesheet.modelview_name}</p>
        //<BootstrapTable data={ timesheet.result } columns={ timesheet.labels } />
    )
    
}

export default Timesheet;