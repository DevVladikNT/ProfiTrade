import axios from 'axios'
import { Card, Flex, Title, Metric, NumberInput, BadgeDelta, AreaChart, Divider, Button } from "@tremor/react";
import { useEffect, useState } from 'react';

let figi = 'BBG006L8G4H1'
let response_ = await axios.get('http://localhost:2000/prices/' + figi);
let arr_ = response_.data.response;
let diff_ = (arr_[arr_.length - 1].close - arr_[arr_.length - 2].close) / arr_[arr_.length - 2].close;
let growth_ = Number((diff_ * 100).toFixed(2));
let direction_ = growth_ > 0 ? "moderateIncrease" : "moderateDecrease";
response_ = await axios.post('http://localhost:3000/predict', {'input': arr_});
let pred_ = response_.data.response;
let pred_diff_ = (pred_ - arr_[arr_.length - 1].close) / arr_[arr_.length - 1].close;
let pred_growth_ = Number((pred_diff_ * 100).toFixed(2));
let pred_direction_ = pred_growth_ > 0 ? "moderateIncrease" : "moderateDecrease";

function PricePlot() {
    let figi = 'BBG006L8G4H1';
    const [history, setHistory] = useState(arr_);
    const [growth, setGrowth] = useState(growth_);
    const [direction, setDirection] = useState(direction_);

    const [pred, setPred] = useState(pred_);
    const [pred_growth, setPredGrowth] = useState(pred_growth_);
    const [pred_direction, setPredDirection] = useState(pred_direction_)

    useEffect(() => {
        const t = setInterval(async () => {
            const response_ = await axios.get('http://localhost:2000/prices/' + figi);
            const history_ = response_.data.response;
            setHistory(history_);
            const prediction_ = await axios.post('http://localhost:3000/predict', {'input': history});
            const pred_ = prediction_.data.response;
            setPred(pred_);

            const diff_ = (history_[history_.length - 1].close - history_[history_.length - 2].close) / history_[history_.length - 2].close;
            const growth_ = Number((diff_ * 100).toFixed(2));
            setGrowth(growth_);
            const dir_ = growth_ > 0 ? "moderateIncrease" : "moderateDecrease";
            setDirection(dir_);

            const pred_diff_ = (pred_ - history_[history_.length - 1].close) / history_[history_.length - 1].close;
            const pred_growth_ = Number((pred_diff_ * 100).toFixed(2));
            setPredGrowth(pred_growth_);
            const pred_dir_ = pred_growth_ > 0 ? "moderateIncrease" : "moderateDecrease";
            setPredDirection(pred_dir_);
        }, 5000)

        return () => {
            clearInterval(t);
        };
    }, []);

    return (
        <Flex flexDirection='col'>
            <Card>
                <Flex flexDirection='row'>
                    <Title>Yandex</Title>
                    <BadgeDelta deltaType={direction}>{Math.abs(growth)}%</BadgeDelta>
                </Flex>
                <Divider>History</Divider>
                <AreaChart
                    className="h-72 mt-4"
                    data={history}
                    index="time"
                    categories={["close"]}
                    colors={["indigo"]}
                    yAxisWidth={40}
                    showXAxis={false}
                    showLegend={false}
                    autoMinValue={true}
                    />
                <Divider>Prediction</Divider>
                <Flex flexDirection='row'>
                    <Metric>{pred}</Metric>
                    <BadgeDelta deltaType={pred_direction}>{Math.abs(pred_growth)}%</BadgeDelta>
                </Flex>
            </Card>
            <Card className="mt-4">
                <Flex flexDirection="row">
                    <Metric className="mr-4">{history[history.length - 1].close}</Metric>
                    <NumberInput placeholder="Amount" min={0}/>
                    <Button className="ml-4" variant="secondary">Sell</Button>
                    <Button className="ml-4">Buy</Button>
                </Flex>
            </Card>
        </Flex>
    );
}

export default PricePlot;