class  CurrentStatement:

    def __init__(self):
        self.start_statemet_day = ""
        self.end_statemet_day = ""
        self.statement_peroid=""
        # self.due_day=""
        self.credit_line = 0
        self.min_payment_all_repaid= 0.0
        self.min_payment_all = 0
        self.min_payment_ins_prin = 0
        # self.min_payment_ins_prin_is_record=False
        self.min_payment_interest=0.0
        self.min_payment_late_interest = 0.0
        self.min_payment_fee_replace = 0.0
        self.min_payment_fee_late_management = 0.0
        self.min_payment_fee_management = 0.0
        self.min_payment_vat = 0.0
        self.min_payment_reverse = 0.0
        # self.min_payment_type={"interest":0.0,"late_interest":0.0,"ins_prin":0.0,"fee_replace":0,"fee_late_management":0,"fee_management":0,"vat":0,"reverse":0}
        self.dq_bucket = -1
        # self.dq_days = 0
        self.purchase_data_all=[]
        self.last_min_payment=0
        self.last_min_payment_had_payoff = False

