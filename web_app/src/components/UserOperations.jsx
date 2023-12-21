import axios from "axios";
import { useEffect, useState } from "react";
import { Card, Title } from "@tremor/react";
import Operation from "./Operation";

function UserOperations(props) {
    const [operations, setOperations] = useState([]);

    useEffect(() => {
        const getData = async () => {
            const response_ = await axios.get('http://localhost:2000/operations/' + props.userId).catch((error) => {
                enqueueSnackbar(error, {variant: 'error'});
            });
            const operations_ = response_.data;
            setOperations(operations_);
        };
        getData();
    }, []);

    useEffect(() => {
        if (props.updateFlag) {
            const getData = async () => {
                const response_ = await axios.get('http://localhost:2000/operations/' + props.userId).catch((error) => {
                    enqueueSnackbar(error, {variant: 'error'});
                });
                const operations_ = response_.data;
                setOperations(operations_);
            };
            getData();
            props.updatedOperations();
        }
    }, [props]);

    return (
        <Card className="ml-4 flex flex-col">
            <Title>History</Title>
            
            <div className="min-h-[100px] flex-[1_1_0] flex flex-col overflow-y-auto">
                {operations.map((operation, index) => (
                    <Operation
                        key={index}
                        figi={operation.figi}
                        price={operation.price}
                        amount={operation.amount}/>
                ))}
            </div>
        </Card>
    );
}

export default UserOperations;