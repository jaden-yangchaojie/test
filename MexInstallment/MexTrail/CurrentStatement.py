class  CurrentStatement:

    def __init__(self):
        self.start_statemet_day = ""
        self.end_statemet_day = ""
        self.statement_peroid=""
        self.start_udi=""
        self.end_udi= ""
        self.flation = 0.0
        self.cycle_day=0
        self.adb_total = {}
        self.adb_record= []
        self.adb = 0
        # self.adb_cal=[]
        # self.due_day=""
        self.credit_line = 0
        self.min_payment_all_repaid= 0.0
        self.min_payment_all = 0


        #分期交易
        self.min_payment_ins_prin = 0
        self.min_payment_ins_interest=0.0
        self.min_payment_ins_vat = 0.0
        #普通交易
        self.min_payment_principal= 0.0
        self.min_payment_vat = 0.0
        self.min_payment_interest=0.0
        self.min_payment_fee_replace = 0.0
        self.min_payment_late_fee = 0.0

        self.init_balance = 0
        self.last_init_balance = 0
        self.end_stmt_posted_bal=0


        #还款退款逆向
        self.min_payment_reverse = 0.0

        self.dq_bucket = -1
        self.dq_is=False
        # self.dq_days = 0
        self.purchase_data_all=[]
        self.last_min_payment=0

        self.last_min_payment_had_payoff = False

