import axios from "axios";
import { useSnackbar } from 'notistack'
import React, { useEffect, useState } from "react";
import { Card, Divider, Text, Title } from "@tremor/react";

import Operation from "./Operation";

function UserOperations(props) {
    const { enqueueSnackbar, closeSnackbar } = useSnackbar();

    const [no_operations, setNoOperations] = useState(false);

    useEffect(() => {
        if (props.updateFlag) {
            const getData = async () => {
                setNoOperations(false);
                const response_ = await axios.get('http://localhost:2000/operations/' + props.user.id).catch((error) => {
                    setNoOperations(true);
                    // enqueueSnackbar('UserOperations\n' + error, {variant: 'error'});
                });
                const operations_ = no_operations ? [] : response_.data;
                props.setOperations(operations_);
            };
            getData();
            props.updatedOperations();
        }
    }, [props]);

    return (
        <Card className="ml-4 min-w-[300px] flex flex-col">
            <Title>History</Title>
            {
                no_operations ?
                <>
                    <Divider />
                    <Text>You haven't bought anything.</Text>
                </> : <></>
                
            }
            <div className="min-h-[100px] flex-[1_1_0] flex flex-col overflow-y-auto">
                {props.operations.map((operation, index) => (
                    props.company.figi === operation.figi ?
                    <Operation
                        {...operation}
                        key={index}
                    /> : <React.Fragment key={index} />
                ))}
            </div>
        </Card>
    );
}

export default UserOperations;