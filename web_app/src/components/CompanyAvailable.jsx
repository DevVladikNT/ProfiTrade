import axios from "axios";
import { Flex, Text, Title, Divider } from "@tremor/react";
import { useEffect, useState } from "react";

function CompanyAvailable(props) {

    const [name, setName] = useState('');

    useEffect(() => {
        const getData = async () => {
            const response = await axios.get('http://localhost:2000/search/' + props.figi);
            const company_name = response.data.response[0].name;
            setName(company_name);
        };
        getData();
    }, []);

    return (
        <Flex flexDirection="row">
            <Title>{name}</Title>
            <Text>x{props.amount}</Text>
        </Flex>
    );
}

export default CompanyAvailable;