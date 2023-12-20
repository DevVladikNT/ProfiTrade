import axios from "axios";
import { useEffect, useState } from "react";
import { Card, Flex, Title, NumberInput, Button, Metric } from "@tremor/react";
import Operation from "./Operation";

function UserOperations(props) {
    const [operations, setOperations] = useState([]);

    useEffect(() => {
        const getData = async () => {
            const response_ = await axios.get('http://localhost:2000/operations/' + props.userId);
            const operations_ = response_.data;
            setOperations(operations_);
        };
        getData();
    }, []);

    useEffect(() => {
        if (props.updateFlag) {
            console.log(`need to update`);
            const getData = async () => {
                const response_ = await axios.get('http://localhost:2000/operations/' + props.userId);
                const operations_ = response_.data;
                setOperations(operations_);
            };
            getData();
            props.updatedOperations();
            console.log(`updated`);
        } else
            console.log(`don't need update`);
    }, [props]);

    return (
        <Card className="ml-4">
            <Title>History</Title>
            {operations.map((operation, index) => (
                <Operation
                    key={index}
                    figi={operation.figi}
                    price={operation.price}
                    amount={operation.amount}/>
            ))}
        </Card>
    );
}

export default UserOperations;