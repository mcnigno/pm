import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
import BootstrapTable from 'react-bootstrap-table-next'
import React, {Component, useEffect,useState} from 'react';
import axios from 'axios';
import ToolkitProvider, { Search, CSVExport } from 'react-bootstrap-table2-toolkit';



class Billable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            timesheet: null,
        };
      }
    componentDidMount() {
        var url = '/timesheetview/api/read'
        axios.get(url)
            .then((response) => {
                var labels = []
                response.data.list_columns.forEach((element,index) => {
                    labels[index]= {
                        text:response.data.label_columns[element], 
                        dataField:element,
                        sort:true
                    }
                
                })
                
                labels.push({
                    dataField: 'action',
                    text: 'Actions',
                    align: 'center',
                    formatter: function () {
                    return (<a href="#" className="like"><i className="fa fa-star"></i></a>)
                    }
                })
                
                response.data['labels'] = labels
                
                this.setState({timesheet: response.data})
                console.log('timesheet result')
                console.log(this.state.timesheet)
        })
    }
    render() {
        if (this.state.timesheet) {
            
            const selectRow = {
                mode: 'checkbox',
                style: { background: 'red' }
              };
            const { SearchBar, ClearSearchButton } = Search;
            const { ExportCSVButton } = CSVExport;
            return  (

                <ToolkitProvider
                    keyField="id"
                    data={ this.state.timesheet.result }
                    columns={ this.state.timesheet.labels }
                    search
                    selectRow={ selectRow }
                    bootstrap4
                >
                {
                    props => (
                    <div>
                        <h3>Input something at below input field:</h3>
                        <SearchBar { ...props.searchProps } />
                        <ClearSearchButton { ...props.searchProps } />
                        <hr />
                        <BootstrapTable
                        { ...props.baseProps} 
                        />
                        <ExportCSVButton { ...props.csvProps }>Export CSV!!</ExportCSVButton>
                    </div>
                    )
                }
                </ToolkitProvider>
                //<p>timesheet</p>
                //<p>{this.state.timesheet.modelview_name}</p>
                /*
                <BootstrapTable 
                    //rowStyle={ { backgroundColor: 'red' } }  
                    keyField='id' 
                    data={ this.state.timesheet.result } 
                    columns={ this.state.timesheet.labels }
                    selectRow={ selectRow } 
                    bootstrap4
                    search
                    />
                    */
            )

        }
        return  (
            <p>no timesheet</p>
            //<p>{timesheet.modelview_name}</p>
            //<BootstrapTable keyField={this.timesheet.result.id} data={ this.state.timesheet.result } columns={ this.state.timesheet.labels } />
        )
    }
}
export default Billable;