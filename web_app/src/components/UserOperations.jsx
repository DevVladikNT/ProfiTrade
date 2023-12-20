import axios from "axios";
import { Card, Flex, NumberInput, Button, Metric } from "@tremor/react";
import Operation from "./Operation";

let user_id = 1;
let response = await axios.get('http://localhost:2000/operations/' + user_id);
let operations = response.data;

function UserOperations() {
    return (
        <Card className="ml-4">
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